import os
from openai import OpenAI
from dotenv import load_dotenv
from agent_state import AgentState

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def synthesiser_node(state: AgentState) -> AgentState:
    try:
        prompt = f"""
        You are a research synthesiser.
        Your job is to combine and synthesise a list of extracted notes from each sub-query.
        Here is the list of extracted notes from each sub-query: {state["sub_query_results"]}.
        These are research findings from multiple sub-queries. Synthesise them into one unified set of notes, preserving all key information.
        """

        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You are a research synthesiser. You combine findings from multiple sources into a single coherent, well-organised set of notes without losing any key information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
        )

        synthesised_notes = response.choices[0].message.content.strip()
        state["extracted_notes"] = synthesised_notes

    except Exception as e:
        print(f"\nError in synthesiser_node: {e}")
        print("\nJoining sub-query results directly...")
        state["extracted_notes"] = "\n".join(state["sub_query_results"])

    return state