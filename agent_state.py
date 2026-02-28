from typing import TypedDict, List

class AgentState(TypedDict):
    query: str
    selected_tool: str
    wikipedia_results: List[str]
    duckduckgo_results: List[str]
    search_results: List[str]
    extracted_notes: str
    final_report: str
    should_continue: bool
    retry_count: int
    search_source: str  # tracks which tool was used