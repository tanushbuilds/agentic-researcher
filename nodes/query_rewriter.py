import ollama
from agent_state import AgentState

def query_rewriter_node(state: AgentState) -> AgentState:
    prompt = f"""
    You are a search query optimizer.
    The following search query returned poor or irrelevant results: "{state['query']}"

    Suggest a single improved search query for the same topic that is more likely to return useful results.
    Reply with ONLY the new query, nothing else. No explanation, no punctuation, just the query.
    """

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content" : prompt}]
    )

    enhanced_query = response["message"]["content"].strip()
    state["query"] = enhanced_query

    return state