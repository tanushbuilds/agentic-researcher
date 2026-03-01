import ollama
import json
import os
from datetime import datetime
from agent_state import AgentState

def write_memory(state: AgentState) -> AgentState:

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            memory = json.load(f)
    else:
        memory = {}

    memory[state["query"]] = {
        "query": state["query"],
        "notes": state["extracted_notes"],
        "timestamp": timestamp,
    }

    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=4)
    
    print(f"\nMemory saved for: '{state['query']}'")

    return state


def read_memory(state: AgentState) -> AgentState:

    try:
        if os.path.exists("memory.json"):
            with open("memory.json", "r") as f:
                memory = json.load(f)
            if memory != {}:
                previous_queries = [memory[i]["query"] for i in memory]

                prompt = f"""
                You are a research assistant.

                Current query: {state["query"]}

                Previous researched topics: {previous_queries}

                Is the current query about the same topic as any of the above?
                Reply with ONLY the exact matching topic from the list, or NONE if no match.
                """

                response = ollama.chat(
                    model="mistral",
                    messages=[{"role": "user", "content": prompt}]
                )

                is_query_match = response["message"]["content"].strip()

                if is_query_match != "NONE" and is_query_match in memory:
                    state["extracted_notes"] = memory[is_query_match]["notes"]
                    state["memory_used"] = True

                    print(f"\nMemory match found: '{is_query_match}'! Skipping search...")
                    
                    return state
                else:
                    print(f"\nNo memory match found. Proceeding with fresh search...")

    except Exception as e:
        print(f"Error in read_memory: {e}")

    state["memory_used"] = False
    return state
