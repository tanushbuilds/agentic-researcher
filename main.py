from agent_state import AgentState
from nodes.search import search_node
from nodes.router import router_node
from nodes.extractor import extraction_node
from nodes.reporter import report_node

MAX_RETRIES = 3

state = AgentState(
    query=input("Enter your research topic: "),
    search_results=[],
    extracted_notes="",
    final_report="",
    should_continue=False,
    retry_count=0
)

# Search loop with router deciding
while state["retry_count"] < MAX_RETRIES:
    state = search_node(state)
    state = router_node(state)

    if state["should_continue"]:
        print("Good results found! Moving on...")
        break
    else:
        state["retry_count"] += 1
        print(f"Results not good enough. Retry {state['retry_count']}/{MAX_RETRIES}...")
        if state["retry_count"] < MAX_RETRIES:
            state["query"] = state["query"] + " overview"  # slightly modify query to try again

# Run extract and report regardless after loop
state = extraction_node(state)
state = report_node(state)

print("=== FINAL REPORT ===")
print(state["final_report"][:1000])