from agent_state import AgentState


def combiner_node(state : AgentState) -> AgentState:
    wikipedia_results = state["wikipedia_results"]
    duckduckgo_results = state["duckduckgo_results"]

    combined_result = f"""
    === WIKIPEDIA ===
    {wikipedia_results}

    === DUCKDUCKGO ===
    {duckduckgo_results}
    """

    state["search_results"] = [combined_result]
    print(f"\n🔗 Combined Wikipedia and DuckDuckGo results!")
    
    return state