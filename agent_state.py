from typing import TypedDict, List

class AgentState(TypedDict):
    query: str
    search_results: List[str]
    extracted_notes: str
    final_report: str
    should_continue: bool
    retry_count: int