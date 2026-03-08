from llm_client import call_llm
from agent_state import AgentState


def report_node(state: AgentState) -> AgentState:
    extracted_notes = state.get("extracted_notes", "")

    # Handle both list and string formats
    if isinstance(extracted_notes, list):
        notes = "\n\n".join(extracted_notes)
    else:
        notes = extracted_notes

    try:
        prompt = f"""
        You are a professional research report writer.

        Write a COMPREHENSIVE and DETAILED research report in clean Markdown format.
        You MUST include ALL information from the research notes below — do not omit, summarize, or skip any detail.
        The report should be as long as necessary to cover every piece of information thoroughly.

        IMPORTANT FORMATTING RULES:
        - Use # for the main title
        - Use ## for major sections
        - Use ### for subsections if needed
        - Use bullet points (-) for lists
        - Use paragraphs for explanations
        - Do NOT include commentary outside the report
        - Do NOT include code fences unless showing code examples
        - Output ONLY the final report in Markdown

        Structure the report as follows:

        # Clear and Concise Report Title

        ## Introduction
        Provide a detailed overview of the topic and full context.

        ## Key Findings
        Cover every finding from the notes. Do not skip anything.

        ## Analysis
        Provide deep explanation, interpretation, and connections between ALL findings.

        ## Conclusion
        Summarize all insights with a clear closing statement.

        ---
        RESEARCH NOTES (use ALL of this information):
        {notes}
        ---
        """

        response = call_llm(prompt, "smart", temperature=0.1)

        state["final_report"] = response.strip()

    except Exception as e:
        print(f"\nError in report_node: {e}")
        state["final_report"] = "Report generation failed."

    return state