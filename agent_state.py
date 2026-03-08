from typing import TypedDict, List


class AgentState(TypedDict):
    query: str
    memory_used: bool
    query_complexity: str
    sub_queries: List[str]
    sub_query_results: List[str]
    wikipedia_results: List[str]
    duckduckgo_results: List[str]
    search_results: List[str]
    extracted_notes: str
    final_report: str
    search_source: str
