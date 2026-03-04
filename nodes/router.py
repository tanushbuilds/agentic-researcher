import os
from openai import OpenAI
from dotenv import load_dotenv
from agent_state import AgentState

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


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

        response = client.chat.completions.create(
            model="gemini-2.5-flash-lite",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=5
        )

        answer = response.choices[0].message.content.strip().upper()

        if answer == "YES":
            state["should_continue"] = True
        else:
            state["should_continue"] = False

    except Exception as e:
        print(f"\nError in router_node: {e}")
        print("\nDefaulting to continue...")
        state["should_continue"] = True

    return state