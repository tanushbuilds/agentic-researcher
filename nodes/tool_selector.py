import ollama
from agent_state import AgentState


def tool_selector_node(state: AgentState) -> AgentState:
    query = state["query"]

    try:

        prompt = f"""
        Decide the best search tool for the following research query.

        Query: "{query}"

        Rules:
        - Choose ONE of: WIKIPEDIA, DUCKDUCKGO, BOTH
        - Reply with ONLY that word, nothing else.

        Guidelines:
        - WIKIPEDIA → historical/factual topics, science concepts, past events/people.
        - DUCKDUCKGO → recent events, trending topics, tech products, practical how-to queries.
        - BOTH → topics with historical context AND recent developments, ongoing events, or living persons.

        Output only a single word: WIKIPEDIA, DUCKDUCKGO, or BOTH.
        """

        response = ollama.chat(
            model="mistral", messages=[{"role": "user", "content": prompt}]
        )

        tool = response["message"]["content"].strip().upper()

        if "BOTH" in tool:
            state["selected_tool"] = "both"
            print("\nTool selected: Both")
        elif "DUCKDUCKGO" in tool:
            state["selected_tool"] = "duckduckgo"
            print("\nTool selected: DuckDuckGo")
        else:
            state["selected_tool"] = "wikipedia"
            print("\nTool selected: Wikipedia")
    except Exception as e:
        print(f"\nError in tool_selector: {e}")
        state["selected_tool"] = "duckduckgo"
        print("\nDefaulting to DuckDuckGo")

    return state
