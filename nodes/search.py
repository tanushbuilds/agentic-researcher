import os
import wikipediaapi
import wikipedia
from openai import OpenAI
from dotenv import load_dotenv
from agent_state import AgentState

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

wiki_wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="AgenticResearchAssistant/1.0 (https://github.com/tanushbuilds/agentic-research-assistant)",
)


def get_best_title(query: str, candidates: list) -> str:

    try:
        prompt = f"""
        You are a Wikipedia title selector.
        A user wants to research: "{query}"

        Choose ONE title from this exact list:
        {chr(10).join(f"{i+1}. {title}" for i, title in enumerate(candidates))}

        RULES:
        - Your answer MUST be copied EXACTLY from the list above, character for character
        - Do NOT modify, combine, or invent any title
        - Do NOT add any explanation
        - If the query exactly matches a title, return that title
        - Otherwise return the single most relevant title from the list

        Reply with ONLY the title, nothing else.
        """

        response = client.chat.completions.create(
            model="gemini-2.5-flash-lite",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=20
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"\nError in get_best_title: {e}")
        return candidates[0]


def search_node(state: AgentState) -> AgentState:
    query = state["query"]

    try:
        candidates = wikipedia.search(query, results=5)

        if not candidates:
            print("\nNo Wikipedia results found at all.")
            state["wikipedia_results"] = ["No results found."]
            return state

        print(f"\nFound {len(candidates)} candidates: {candidates}")

        best_title = get_best_title(query, candidates)
        print(f"\nLLM picked: '{best_title}'")

        page = wiki_wiki.page(best_title)

        if page.exists():
            print(f"\nPage found!")
            state["wikipedia_results"] = [page.text]
        else:
            print(f"\nLLM pick not found, using first candidate: '{candidates[0]}'")
            page = wiki_wiki.page(candidates[0])
            if page.exists():
                state["wikipedia_results"] = [page.text]
            else:
                state["wikipedia_results"] = ["No results found."]

    except Exception as e:
        print(f"\nError in search_node: {e}")
        state["wikipedia_results"] = ["No results found."]

    return state