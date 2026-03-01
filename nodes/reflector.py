import ollama
from agent_state import AgentState


def reflector_node(state: AgentState) -> AgentState:

    try:
        prompt = f"""
        You are a research quality checker.

        User's research query: {state["query"]}

        Report: {state["final_report"]}

        Your job is to judge the report on two things:
        - Does it actually answer the original query?
        - Is it detailed enough to be useful?

        Reply with ONLY ONE word: APPROVED or REJECTED

        Nothing else
        """

        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )

        report_approved = response["message"]["content"].strip()

        state["report_approved"] = True if report_approved == "APPROVED" else False

        if state["report_approved"]:
            print(f"\nReport approved!")
        else:
            print(f"\nReport rejected — rewriting...")

    except Exception as e:
        print(f"Error in reflector_node: {e}")
        print("Defaulting to approved...")
        state["report_approved"] = True

    return state