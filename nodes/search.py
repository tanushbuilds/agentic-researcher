from agent_state import AgentState
import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='AgenticResearchAssistant/1.0 (https://github.com/tanushbuilds/agentic-research-assistant)'
)

def search_node(state: AgentState) -> AgentState:
    topic = state['query']
    page = wiki_wiki.page(topic)
    
    if page.exists():
        # Grab first 1000 characters to keep it short
        state['search_results'] = [page.text[:1000]]
    else:
        state['search_results'] = ["No results found."]
    
    return state