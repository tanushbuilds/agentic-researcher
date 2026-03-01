import ollama
from agent_state import AgentState

def report_node(state: AgentState) -> AgentState:
    notes = "\n\n".join([state.get("extracted_notes", "")])

    try:
        prompt = f"""
        You are a research assistant.
        Write a full, structured research report based on the following notes:

        {notes}

        Include:
        - Introduction
        - Key Findings
        - Analysis
        - Conclusion
        """

        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )

        report = response["message"]["content"]
        state["final_report"] = report
    except Exception as e:
        print(f"\nError in report_node: {e}")
        state["final_report"] = "Report generation failed."

    return state