from concurrent.futures import ThreadPoolExecutor
from .search import search_node
from .duckduckgo import duckduckgo_node
import copy


def parallel_search_node(state):
    # Create copies so threads don’t mutate same object
    state_for_wiki = copy.deepcopy(state)
    state_for_ddg = copy.deepcopy(state)

    with ThreadPoolExecutor(max_workers=2) as executor:
        wiki_future = executor.submit(search_node, state_for_wiki)
        ddg_future = executor.submit(duckduckgo_node, state_for_ddg)

        wiki_result = wiki_future.result()
        ddg_result = ddg_future.result()

    # Merge results back into original state
    state["wikipedia_results"] = wiki_result.get("wikipedia_results")
    state["duckduckgo_results"] = ddg_result.get("duckduckgo_results")
    state["search_source"] = "parallel (duckduckgo and wikipedia)"

    return state