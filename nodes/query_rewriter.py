import os
from openai import OpenAI
from dotenv import load_dotenv
from agent_state import AgentState

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def query_rewriter_node(state: AgentState) -> AgentState:
    original_query = state["query"]
    try:
        prompt = f"""
        You are a search query optimizer.
        The following search query returned poor or irrelevant results: "{state['query']}"

        Suggest a single improved search query for the same topic that is more likely to return useful results.
        Reply with ONLY the new query, nothing else. No explanation, no punctuation, just the query.
        """

        response = client.chat.completions.create(
            model="gemini-2.5-flash-lite",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=30
        )

        enhanced_query = response.choices[0].message.content.strip()
        state["query"] = enhanced_query

    except Exception as e:
        print(f"\nError in query_rewriter: {e}")
        print("\nKeeping original query...")
        state["query"] = original_query

    return state