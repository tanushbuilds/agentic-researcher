from agent_state import AgentState
from nodes.search import search_node
from nodes.router import router_node
from nodes.extractor import extraction_node
from nodes.reporter import report_node
from nodes.duckduckgo import duckduckgo_node
from nodes.tool_selector import tool_selector_node
from nodes.query_rewriter import query_rewriter_node
from nodes.combiner import combiner_node


MAX_RETRIES = 3

state = AgentState(
    query=input("Enter your research topic: "),
    wikipedia_results=[],
    duckduckgo_results=[],
    search_results=[],
    extracted_notes="",
    final_report="",
    should_continue=False,
    retry_count=0,
    search_source="",
    selected_tool=""
)

original_query = state["query"]

# Step 1 — LLM selects the tool
state = tool_selector_node(state)
primary_tool = state["selected_tool"]
fallback_tool = "duckduckgo" if primary_tool == "wikipedia" else "wikipedia"

# Step 2 — helper to run the right search node
def run_search(state, tool):

    if state["selected_tool"] == "both":
        print("\nSearching both tools...")
        state = search_node(state)
        state = duckduckgo_node(state)
        state = combiner_node(state)
        print("\nBoth sources combined! Moving on...")
        state["should_continue"] = True

        return state

    elif tool == "wikipedia":
        return search_node(state)

    else:
        return duckduckgo_node(state)

# Step 3 — try primary tool
print(f"\nPrimary tool: {primary_tool}...")

if state["selected_tool"] == "both":
    state = run_search(state, "both")
else:
    while state["retry_count"] < MAX_RETRIES:
        state = run_search(state, primary_tool)
        state = router_node(state)

        if state["should_continue"]:
            print(f"\n{primary_tool.title()} results good! Moving on...")
            break
        else:
            state["retry_count"] += 1
            print(f"\n{primary_tool.title()} retry {state['retry_count']}/{MAX_RETRIES}...")
            if state["retry_count"] < MAX_RETRIES:
                state = query_rewriter_node(state)
                print(f"Enhanced query: {state["query"]}")

# Step 4 — fall back to other tool if primary failed
if not state["should_continue"]:
    print(f"\nFalling back to {fallback_tool}...")
    state["query"] = original_query
    state["retry_count"] = 0
    state = run_search(state, fallback_tool)
    state = router_node(state)

    if state["should_continue"]:
        print(f"\n{fallback_tool.title()} results good! Moving on...")
    else:
        print("\nBoth tools struggled, proceeding with what we have...")


# Step 5 — extract and report
state = extraction_node(state)
state = report_node(state)

print(f"\n=== FINAL REPORT (source: {state['search_source']}) ===")
print(f"\n{state["final_report"]}")