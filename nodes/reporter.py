import ollama
from agent_state import AgentState


def report_node(state: AgentState) -> AgentState:
    notes = "\n\n".join([state.get("extracted_notes", "")])

    try:
        prompt = f"""
        You are a professional research report writer.

        Write a complete, well-structured research report in clean Markdown format.

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
        Provide a brief overview of the topic and context.

        ## Key Findings
        Present the most important findings as structured bullet points with short explanations.

        ## Analysis
        Provide deeper explanation, interpretation, and connections between findings.

        ## Conclusion
        Summarize the insights and provide a clear closing statement.

        Research Notes:
        {notes}
        """

        response = ollama.chat(
            model="mistral", messages=[{"role": "user", "content": prompt}]
        )

        report = response["message"]["content"]
        state["final_report"] = report
    except Exception as e:
        print(f"\nError in report_node: {e}")
        state["final_report"] = "Report generation failed."

    return state
