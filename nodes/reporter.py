import ollama
from agent_state import AgentState  # updated from agent_state.py

def report_node(state: AgentState) -> AgentState:
    notes = "\n\n".join([state.get("extracted_notes", "")])

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

    return state