import ollama
from agent_state import AgentState

def query_classifier_node(state: AgentState) -> AgentState:
    
    prompt = f"""
    You are a research assistant.
    Your job is to detect if the user's research query is COMPLEX or SIMPLE.
    Research Query: {state["query"]}
    Reply with ONLY one word: COMPLEX or SIMPLE
    """
    
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    query_complexity = response["message"]["content"].strip()
    state["query_complexity"] = query_complexity
    
    return state