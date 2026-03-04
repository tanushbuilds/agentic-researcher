from agent_state import AgentState
from llm_client import call_llm


def synthesiser_node(state: AgentState) -> AgentState:
    try:
        prompt = f"""
        You are a research synthesiser.
        Your job is to combine and synthesise a list of extracted notes from each sub-query.
        Here is the list of extracted notes from each sub-query: {state["sub_query_results"]}.
        These are research findings from multiple sub-queries. Synthesise them into one unified set of notes, preserving all key information.
        """

        synthesised_notes = call_llm(
            prompt, mode="smart", temperature=0.1
        ).strip()

        state["extracted_notes"] = synthesised_notes

    except Exception as e:
        print(f"\nError in synthesiser_node: {e}")
        print("\nJoining sub-query results directly...")
        state["extracted_notes"] = "\n".join(state["sub_query_results"])

    return state