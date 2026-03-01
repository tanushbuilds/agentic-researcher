import ollama
from agent_state import AgentState

def extraction_node(state: AgentState) -> AgentState:
    text_to_summarize = "\n\n".join(state.get("search_results", []))

    try:
        prompt = f"""
        You are extracting research notes about: "{state['query']}"

        STRICT RULES:
        - Extract ONLY facts directly about "{state['query']}"
        - If the text contains ANYTHING unrelated to "{state['query']}", completely ignore it
        - Do NOT comment on the format or structure of the text
        - Do NOT say "you have provided" or "it appears" 
        - Just extract the relevant facts as a clean numbered list
        - If you find no relevant facts, say "No relevant information found"

        Text:
        {text_to_summarize}
        """

        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )

        summary = response["message"]["content"]
        state["extracted_notes"] = summary
    except Exception as e:
        print(f"\nError in extraction_node: {e}")
        state["extracted_notes"] = "No notes extracted."


    return state