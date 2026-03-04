import os
from openai import OpenAI
from dotenv import load_dotenv
from agent_state import AgentState

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


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

        response = client.chat.completions.create(
            model="gemini-2.5-flash-lite",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=5
        )

        tool = response.choices[0].message.content.strip().upper()

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