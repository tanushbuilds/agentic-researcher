from typing import TypedDict, List

class AgentState(TypedDict):
    query: str
    memory_used: bool
    query_complexity: str
    sub_queries: List[str]
    selected_tool: str
    sub_query_results: List[str]
    wikipedia_results: List[str]
    duckduckgo_results: List[str]
    search_results: List[str]
    extracted_notes: str
    final_report: str
    report_approved: bool
    reflection_count: int
    should_continue: bool
    retry_count: int
    search_source: str