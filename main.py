from agent_state import AgentState
from nodes.search import search_node
from nodes.extractor import extraction_node

state = AgentState(
    query="Artificial intelligence in education",
    search_results=[],
    extracted_notes="",
    final_report=""
)

state = search_node(state)
state = extraction_node(state)

print(state['extracted_notes'][:500])  # First 500 chars of summary