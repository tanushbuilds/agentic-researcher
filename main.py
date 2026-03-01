from agent_state import AgentState
from nodes.search import search_node
from nodes.router import router_node
from nodes.extractor import extraction_node
from nodes.reporter import report_node
from nodes.duckduckgo import duckduckgo_node
from nodes.tool_selector import tool_selector_node
from nodes.query_rewriter import query_rewriter_node
from nodes.combiner import combiner_node
from nodes.query_classifier import query_classifier_node
from nodes.planner import planner_node
from nodes.synthesiser import synthesiser_node
from nodes.memory import read_memory, write_memory


MAX_RETRIES = 3

state = AgentState(
    query=input("Enter your research topic: "),
    query_complexity="",
    sub_queries=[],
    sub_query_results=[],
    wikipedia_results=[],
    duckduckgo_results=[],
    search_results=[],
    extracted_notes="",
    final_report="",
    should_continue=False,
    retry_count=0,
    search_source="",
    selected_tool="",
    memory_used=False,
)

def display_final_report():
    print(f"\n=== FINAL REPORT (source: {state['search_source']}) ===")
    print(f"\n{state["final_report"]}")



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

def agentic_research(state, original_query) -> AgentState:
    state = tool_selector_node(state)
    primary_tool = state["selected_tool"]
    fallback_tool = "duckduckgo" if primary_tool == "wikipedia" else "wikipedia"
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
                    print(f"\nEnhanced query: {state["query"]}")

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

    return state


original_query = state["query"]


state = read_memory(state)

if state["memory_used"]:
    print("\nUsing cached memory! Skipping search...")
    state = report_node(state)
    display_final_report()

else:
    state = query_classifier_node(state)
    query_complexity = state["query_complexity"]

    if query_complexity == "COMPLEX":
        state = planner_node(state)
        sub_queries = state["sub_queries"]
        for sub_query in sub_queries:
            state["query"] = sub_query

            state["retry_count"] = 0
            state["should_continue"] = False
            state["wikipedia_results"] = []
            state["duckduckgo_results"] = []
            state["search_results"] = []
            state["extracted_notes"] = ""  
            
            state = agentic_research(state, sub_query)
            state["sub_query_results"].append(state["extracted_notes"])
        
        print(f"\nSub query results: {state['sub_query_results']}")
        state = synthesiser_node(state)
        state["query"] = original_query


    else:
        state = agentic_research(state, original_query)
    
    state = report_node(state)
    state = write_memory(state)
    display_final_report()
