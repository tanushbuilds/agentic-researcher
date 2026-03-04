from agent_state import AgentState
from llm_client import call_llm


def router_node(state: AgentState) -> AgentState:
    query = state.get("query", "")
    search_results = "\n\n".join(state.get("search_results", []))

    try:
        prompt = f"""
        You are a research quality checker.
        A researcher searched for: "{query}"
        
        Here are the search results they got:
        {search_results}
        
        Are these results useful and relevant enough to write a research report?
        Reply with ONLY one word: YES or NO.
        """

        answer = call_llm(
            prompt, mode="fast", temperature=0.0, max_tokens=5
        ).strip().upper()

        state["should_continue"] = answer == "YES"

    except Exception as e:
        print(f"\nError in router_node: {e}")
        print("\nDefaulting to continue...")
        state["should_continue"] = True

    return state