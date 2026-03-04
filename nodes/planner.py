import re
from agent_state import AgentState
from llm_client import call_llm


def planner_node(state: AgentState) -> AgentState:

    try:
        prompt = f"""
        You are a research query planner.
        Break this query into a maximum of 3 short, search-engine-friendly sub-queries: "{state["query"]}"

        Rules:
        - Each sub-query must be 3-6 words only
        - No full sentences or questions
        - Return ONLY a numbered list, one per line
        - No explanations, no extra text
        """

        lines = call_llm(
            prompt, mode="fast", temperature=0.0, max_tokens=100
        ).strip().split("\n")

        sub_queries = []
        for line in lines:
            cleaned = re.sub(r'^[\d]+[.)]\s*|^[-•]\s*', '', line).strip()
            if cleaned:
                sub_queries.append(cleaned)

        state["sub_queries"] = sub_queries
        print(f"\nSub-queries: {sub_queries}")

    except Exception as e:
        print(f"\nError in planner_node: {e}")
        print("\nTreating original query as single sub-query...")
        state["sub_queries"] = [state["query"]]

    return state