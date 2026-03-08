from agent_state import AgentState
from llm_client import call_llm

EXTRACTION_FORMAT = """
Format each fact as:
BAD:  "Ronaldo is a famous footballer who was born in Portugal"
GOOD: "Ronaldo | 41 years old | Portugal | 965 goals"
"""

def extraction_node(state: AgentState) -> AgentState:
    text_to_summarize = "\n\n".join(state.get("search_results", []))

    try:
        prompt = f"""
        You are extracting research notes about: "{state['query']}"

        {EXTRACTION_FORMAT}

        Text:
        {text_to_summarize}
        """


        response = call_llm(prompt, "smart", temperature=0.1)
        state["extracted_notes"] = response.strip()

    except Exception as e:
        print(f"\nError in extraction_node: {e}")
        state["extracted_notes"] = "No notes extracted."

    return state