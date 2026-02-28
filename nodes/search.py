import ollama
import wikipediaapi
import wikipedia
from agent_state import AgentState

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='AgenticResearchAssistant/1.0 (https://github.com/tanushbuilds/agentic-research-assistant)'
)

def get_best_title(query: str, candidates: list) -> str:
    prompt = f"""
    A user wants to research: "{query}"
    
    Here are Wikipedia page titles related to this topic:
    {chr(10).join(f"{i+1}. {title}" for i, title in enumerate(candidates))}
    
    Your job is to pick the MOST SPECIFIC and RELEVANT title for the query.
    If a title exactly matches the user's query, prioritise that above all others.
    
    Reply with ONLY the exact title from the list, nothing else.
    No explanation, no punctuation, just the title.
    """
    
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["message"]["content"].strip()

def search_node(state: AgentState) -> AgentState:
    query = state['query']
    
    # Step 1 — Get 10 candidate titles from Wikipedia
    candidates = wikipedia.search(query, results=20)
    
    if not candidates:
        print("\nNo Wikipedia results found at all.")
        state['wikipedia_results'] = ["No results found."]
        return state
    
    print(f"\nFound {len(candidates)} candidates: {candidates}")
    
    # Step 2 — Ask LLM to pick the best one
    best_title = get_best_title(query, candidates)
    print(f"\nLLM picked: '{best_title}'")
    
    # Step 3 — Fetch that page
    page = wiki_wiki.page(best_title)
    
    if page.exists():
        print(f"\nPage found!")
        state['wikipedia_results'] = [page.text[:3000]]
    else:
        # Fallback — just use the first candidate
        print(f"\nLLM pick not found, using first candidate: '{candidates[0]}'")
        page = wiki_wiki.page(candidates[0])
        if page.exists():
            state['wikipedia_results'] = [page.text[:3000]]
        else:
            state['wikipedia_results'] = ["No results found."]
    
    return state