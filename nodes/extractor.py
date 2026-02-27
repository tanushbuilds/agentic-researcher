import ollama
from agent_state import AgentState

def extraction_node(state: AgentState) -> AgentState:
    text_to_summarize = "\n\n".join(state.get("search_results", []))

    prompt = f"""
    You are a research assistant.
    Extract the key points from the following text
    and present them as a structured list of notes:

    {text_to_summarize}
    """

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response["message"]["content"]
    state["extracted_notes"] = summary

    return state