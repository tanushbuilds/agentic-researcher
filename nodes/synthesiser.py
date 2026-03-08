from llm_client import call_llm
from agent_state import AgentState

SYNTHESIS_FORMAT = """
Combine all facts into compact format, one entity/topic per line:
BAD:  "Ronaldo is a famous footballer who has scored many goals throughout his career"
GOOD: "Ronaldo | 41 years old | Portugal | 965 goals | 5 Ballon d'Or"

- Merge duplicate facts across sources
- Keep ALL unique details, nothing dropped
- No prose, no commentary, just compact fact strings
"""

def synthesiser_node(state: AgentState) -> AgentState:
    try:
        prompt = f"""
        You are a research synthesiser for the topic: "{state['query']}"

        {SYNTHESIS_FORMAT}

        Extracted notes from each sub-query:
        {state["sub_query_results"]}
        """

        response = call_llm(prompt, "smart", temperature=0.1)
        state["extracted_notes"] = response.strip()

    except Exception as e:
        print(f"\nError in synthesiser_node: {e}")
        state["extracted_notes"] = "\n".join(state["sub_query_results"])

    return state