from agent_state import AgentState
from nodes.search import search_node
from nodes.extractor import extraction_node
from nodes.reporter import report_node

# Initialize state
state = AgentState(
    query="Artificial intelligence in education",
    search_results=[],
    extracted_notes="",
    final_report=""
)

# Run agent nodes
state = search_node(state)
state = extraction_node(state)
state = report_node(state)

# Print outputs
print("=== FINAL REPORT ===")
print(state['final_report'][:1000])  # first 1000 chars