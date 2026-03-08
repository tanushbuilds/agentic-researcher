from agent_state import AgentState
from nodes.extractor import extraction_node
from nodes.reporter import report_node
from nodes.combiner import combiner_node
from nodes.planner import planner_node
from nodes.synthesiser import synthesiser_node
from nodes.memory import write_memory
from nodes.parallel_search_node import parallel_search_node


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
        search_source="",
        memory_used=False,
    )
    
    # Step 2 — helper to run the right search node
    def run_search(state):
            send("Searching both tools...")
            state = parallel_search_node(state)
            state = combiner_node(state)
            send("Both sources combined! Moving on...")
            return state



    def agentic_research(state) -> AgentState:
        state = run_search(state)
        state = extraction_node(state)

        return state


    original_query = state["query"]


    state = planner_node(state)

    if state["memory_used"]:
        send("Using cached memory! Skipping search...")
        state = report_node(state)

    else:
        if state["query_complexity"] == "COMPLEX":
            sub_queries = state["sub_queries"]
            state["sub_query_results"] = []
            for i, sub_query in enumerate(sub_queries):
                send(f"Researching sub-query {i+1}/{len(sub_queries)}: {sub_query}...", "active")
                state["query"] = sub_query
                state["wikipedia_results"] = []
                state["duckduckgo_results"] = []
                state["search_results"] = []
                state["extracted_notes"] = ""

                state = agentic_research(state)
                state["sub_query_results"].append(state["extracted_notes"])

            send("All sub-queries complete! Synthesising...", "active")
            state = synthesiser_node(state)
            state["query"] = original_query

        else:
            state = agentic_research(state)

        state = report_node(state)
        state = write_memory(state)

    return state



