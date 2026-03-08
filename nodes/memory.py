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
