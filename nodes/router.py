import ollama
from agent_state import AgentState

def router_node(state: AgentState) -> AgentState:
    search_results = "\n\n".join(state.get("search_results", []))
    query = state.get("query", "")

    prompt = f"""
    You are a research quality checker.
    A researcher searched for: "{query}"
    
    Here are the search results they got:
    {search_results}
    
    Are these results useful and relevant enough to write a research report?
    Reply with ONLY one word: YES or NO.
    """

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response["message"]["content"].strip().upper()

    if answer == "YES":
        state["should_continue"] = True
    else:
        state["should_continue"] = False

    return state