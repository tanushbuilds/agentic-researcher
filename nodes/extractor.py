from agent_state import AgentState
from llm_client import call_llm


def extraction_node(state: AgentState) -> AgentState:
    text_to_summarize = "\n\n".join(state.get("search_results", []))
    print(text_to_summarize)
    try:
        prompt = f"""
        You are a research evidence extraction engine.

        Your task is to extract **all relevant information** about "{state['query']}" from the provided text. 
        Nothing should be removed, summarized, or shortened — preserve full depth, context, dates, statistics, awards, achievements, controversies, criticisms, and personal details if available.

        CRITICAL INSTRUCTIONS:

        - Include **everything** relevant; do NOT compress or remove information.
        - Each fact gets its own line. If a paragraph contains multiple facts, create multiple lines.
        - Include dates, numbers, stats, awards, records, clubs, teams, controversies, and personal life details.
        - Only exclude content that is **clearly unrelated** to "{state['query']}".

        Text:
        {text_to_summarize}
        """

        summary = call_llm(prompt, mode="smart", temperature=0.1)
        state["extracted_notes"] = summary

    except Exception as e:
        print(f"\nError in extraction_node: {e}")
        state["extracted_notes"] = "No notes extracted."

    return state