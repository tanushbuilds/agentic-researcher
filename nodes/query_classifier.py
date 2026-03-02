import ollama
from agent_state import AgentState


def query_classifier_node(state: AgentState) -> AgentState:

    try:
        prompt = f"""
        You are a query complexity classifier.

        SIMPLE: The query is about a single entity, person, place, or fact.
        COMPLEX: The query requires comparison, analysis, or research across multiple entities or topics.

        Query: {state["query"]}

        Reply with ONLY one word: COMPLEX or SIMPLE
        """

        response = ollama.chat(
            model="mistral", messages=[{"role": "user", "content": prompt}]
        )

        query_complexity = response["message"]["content"].strip()
        state["query_complexity"] = query_complexity
    except Exception as e:
        print(f"\nError in query_classifier: {e}")
        print("\nDefaulting to SIMPLE...")
        state["query_complexity"] = "SIMPLE"

    return state
