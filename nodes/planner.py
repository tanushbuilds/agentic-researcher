import ollama
from agent_state import AgentState

def planner_node(state: AgentState) -> AgentState:
    prompt = f"""
    You are a research query planner.
    Break this query into a maximum of 3 short, search-engine-friendly sub-queries: "{state["query"]}"

    Rules:
    - Each sub-query must be 3-6 words only
    - No full sentences or questions
    - Return ONLY a numbered list, one per line
    - No explanations, no extra text
    """
    
    response = ollama.chat(
        model="mistral",
        messages=[{"role":"user", "content": prompt}]
    )
    sub_queries = response["message"]["content"].strip().split("\n")
    sub_queries = list(sub_queries[i].split(". ")[1] for i in range(len(sub_queries)))

    state["sub_queries"] = sub_queries
    print(sub_queries)

    return state