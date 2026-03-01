import ollama
from agent_state import AgentState

def tool_selector_node(state: AgentState) -> AgentState:
    query = state['query']

    try:

        prompt = f"""
        You are deciding which search tool to use for a research query.
        
        Query: "{query}"
        
        WIKIPEDIA is better for:
        - Established, factual, historical topics
        - Scientific concepts
        - People, places, events from the past
        - Example: "Milky Way", "World War 2", "Photosynthesis"
        
        DUCKDUCKGO is better for:
        - Recent or current topics
        - Practical how-to queries
        - Technology products or tools
        - Trending topics
        - Example: "Latest AI Trends", "How to use Claude AI", "Best Python libraries 2026"

        BOTH is better when:
        - The topic has both a rich historical background AND recent developments
        - The topic is a living person, ongoing event, or evolving technology
        - You need both foundational knowledge and current information
        
        Reply with ONLY one word: WIKIPEDIA, DUCKDUCKGO or BOTH
        """

        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )


        tool = response["message"]["content"].strip().upper()

        if "BOTH" in tool:
            state['selected_tool'] = "both"
            print("\nTool selected: Both")
        elif "DUCKDUCKGO" in tool:
            state['selected_tool'] = "duckduckgo"
            print("\nTool selected: DuckDuckGo")
        else:
            state['selected_tool'] = "wikipedia"
            print("\nTool selected: Wikipedia")
    except Exception as e:
        print(f"Error in tool_selector: {e}")
        state["selected_tool"] = "duckduckgo"
        print("Defaulting to DuckDuckGo")

    return state