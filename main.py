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
from nodes.reflector import reflector_node


def run_agent(query: str, send=None) -> AgentState:
    
    # default send to print if not provided
    # this way terminal still works without Django
    if send is None:
        send = lambda message, status='default': print(message)
    
    state = AgentState(
        query=query,
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
        report_approved=False,
        reflection_count=0,
    )
    
    MAX_RETRIES = 3
    MAX_REFLECTIONS = 2





    # Step 2 — helper to run the right search node
    def run_search(state, tool):

        if state["selected_tool"] == "both":
            send("Searching both tools...")
            state = search_node(state)
            state = duckduckgo_node(state)
            state = combiner_node(state)
            send("Both sources combined! Moving on...")
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
        send(f"Primary tool: {primary_tool}...")
        if state["selected_tool"] == "both":
            state = run_search(state, "both")
        else:
            while state["retry_count"] < MAX_RETRIES:
                state = run_search(state, primary_tool)
                state = router_node(state)

                if state["should_continue"]:
                    send(f"{primary_tool.title()} results good! Moving on...")
                    break
                else:
                    state["retry_count"] += 1
                    send(
                        f"{primary_tool.title()} retry {state['retry_count']}/{MAX_RETRIES}..."
                    )
                    if state["retry_count"] < MAX_RETRIES:
                        state = query_rewriter_node(state)
                        send(f"Enhanced query: {state["query"]}")

        # Step 4 — fall back to other tool if primary failed
        if not state["should_continue"]:
            send(f"Falling back to {fallback_tool}...")
            state["query"] = original_query
            state["retry_count"] = 0
            state = run_search(state, fallback_tool)
            state = router_node(state)

            if state["should_continue"]:
                send(f"{fallback_tool.title()} results good! Moving on...")
            else:
                send("Both tools struggled, proceeding with what we have...")

        # Step 5 — extract and report
        state = extraction_node(state)

        return state


    original_query = state["query"]


    state = read_memory(state)

    if state["memory_used"]:
        send("Using cached memory! Skipping search...")
        state = report_node(state)

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

            send("All sub-queries complete! Synthesising...", "active")
            state = synthesiser_node(state)
            state["query"] = original_query

        else:
            state = agentic_research(state, original_query)

        state = report_node(state)
        state = reflector_node(state)

        while not state["report_approved"] and state["reflection_count"] < MAX_REFLECTIONS:
            state["reflection_count"] += 1
            send(f"Reflection attempt {state['reflection_count']}/{MAX_REFLECTIONS}...")
            state["retry_count"] = 0
            state["should_continue"] = False
            state = agentic_research(state, original_query)
            state = report_node(state)
            state = reflector_node(state)

        state = write_memory(state)

        
    return state

