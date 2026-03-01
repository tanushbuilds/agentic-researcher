import ollama
import wikipediaapi
import wikipedia
from agent_state import AgentState

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='AgenticResearchAssistant/1.0 (https://github.com/tanushbuilds/agentic-research-assistant)'
)

def get_best_title(query: str, candidates: list) -> str:

    try:
        prompt = f"""
        You are a Wikipedia title selector.
        A user wants to research: "{query}"

        Here are the ONLY available Wikipedia page titles to choose from:
        {chr(10).join(f"{i+1}. {title}" for i, title in enumerate(candidates))}

        Rules:
        - You MUST pick exactly ONE title from the list above
        - Do NOT invent or combine titles
        - If a title exactly matches the query, pick that one
        - Otherwise pick the MOST SPECIFIC and RELEVANT title from the list
        - If no title is relevant, pick the closest match

        Reply with ONLY the exact title as it appears in the list above, nothing else.
        """
        
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"\nError in get_best_title: {e}")
        return candidates[0]  # fallback to first candidate

def search_node(state: AgentState) -> AgentState:
    query = state['query']
    
    try:

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
            state['wikipedia_results'] = [page.text[:750]]
        else:
            # Fallback — just use the first candidate
            print(f"\nLLM pick not found, using first candidate: '{candidates[0]}'")
            page = wiki_wiki.page(candidates[0])
            if page.exists():
                state['wikipedia_results'] = [page.text[:750]]
            else:
                state['wikipedia_results'] = ["No results found."]
    except Exception as e:
        print(f"\nError in search_node: {e}")
        state['wikipedia_results'] = ["No results found."]

    return state