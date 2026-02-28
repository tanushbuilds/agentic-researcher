from ddgs import DDGS
from agent_state import AgentState

def duckduckgo_node(state: AgentState) -> AgentState:
    query = state['query']
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        
        if not results:
            print("\nDuckDuckGo found nothing.")
            state['duckduckgo_results'] = ["No results found."]
            state['duckduckgo_results'] = "duckduckgo"
            return state
        
        # Combine the body text from top results
        combined = "\n\n".join([
            f"Source: {r['href']}\n{r['body']}"
            for r in results if r.get('body')
        ])
        
        print(f"\nDuckDuckGo found {len(results)} results!")
        state['duckduckgo_results'] = [combined]
        state['search_source'] = "duckduckgo"
    
    except Exception as e:
        print(f"\nDuckDuckGo error: {e}")
        state['duckduckgo_results'] = ["No results found."]
        state['search_source'] = "duckduckgo"
    
    return state