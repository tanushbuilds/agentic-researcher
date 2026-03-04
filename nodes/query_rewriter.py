from agent_state import AgentState
from llm_client import call_llm


def query_rewriter_node(state: AgentState) -> AgentState:
    original_query = state["query"]
    try:
        prompt = f"""
        You are a search query optimizer.
        The following search query returned poor or irrelevant results: "{state['query']}"

        Suggest a single improved search query for the same topic that is more likely to return useful results.
        Reply with ONLY the new query, nothing else. No explanation, no punctuation, just the query.
        """

        enhanced_query = call_llm(
            prompt, mode="fast", temperature=0.3, max_tokens=30
        ).strip()

        state["query"] = enhanced_query

    except Exception as e:
        print(f"\nError in query_rewriter: {e}")
        print("\nKeeping original query...")
        state["query"] = original_query

    return state