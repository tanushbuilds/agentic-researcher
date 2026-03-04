from agent_state import AgentState
from llm_client import call_llm


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

        report_approved = call_llm(
            prompt, mode="fast", temperature=0.0, max_tokens=5
        ).strip()

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