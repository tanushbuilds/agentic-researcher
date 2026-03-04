import os
from openai import OpenAI
from dotenv import load_dotenv
from agent_state import AgentState

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def query_classifier_node(state: AgentState) -> AgentState:

    try:
        prompt = f"""
        You are a query complexity classifier.

        SIMPLE: The query is about a single entity, person, place, or fact.
        COMPLEX: The query requires comparison, analysis, or research across multiple entities or topics.

        Query: {state["query"]}

        Reply with ONLY one word: COMPLEX or SIMPLE
        """

        response = client.chat.completions.create(
            model="gemini-2.5-flash-lite",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=5
        )

        query_complexity = response.choices[0].message.content.strip()
        state["query_complexity"] = query_complexity

    except Exception as e:
        print(f"\nError in query_classifier: {e}")
        print("\nDefaulting to SIMPLE...")
        state["query_complexity"] = "SIMPLE"

    return state