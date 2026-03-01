import ollama
from agent_state import AgentState


def synthesiser_node(state: AgentState) -> AgentState:
    try:
        prompt = f"""
        You are a research assistant.
        Your job is to combine and synthesise a list of extracted notes from each sub-query.
        Here is the list of extracted notes from each sub-query: {state["sub_query_results"]}.
        These are research findings from multiple sub-queries. Synthesise them into one unified set of notes, preserving all key information.
        """

        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )

        synthesised_notes = response["message"]["content"].strip()
        state["extracted_notes"] = synthesised_notes
    except Exception as e:
        print(f"Error in synthesiser_node: {e}")
        print("Joining sub-query results directly...")
        state["extracted_notes"] = "\n".join(state["sub_query_results"])

    return state