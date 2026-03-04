from agent_state import AgentState
from llm_client import call_llm


def query_classifier_node(state: AgentState) -> AgentState:

    try:
        prompt = f"""
        You are a query complexity classifier.

        SIMPLE: The query is about a single entity, person, place, or fact.
        COMPLEX: The query requires comparison, analysis, or research across multiple entities or topics.

        Query: {state["query"]}

        Reply with ONLY one word: COMPLEX or SIMPLE
        """

        query_complexity = call_llm(
            prompt, mode="fast", temperature=0.0, max_tokens=5
        ).strip()

        state["query_complexity"] = query_complexity

    except Exception as e:
        print(f"\nError in query_classifier: {e}")
        print("\nDefaulting to SIMPLE...")
        state["query_complexity"] = "SIMPLE"

    return state