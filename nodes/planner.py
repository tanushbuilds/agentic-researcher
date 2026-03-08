from llm_client import call_llm
import os
import json
from agent_state import AgentState
import re


def planner_node(state: AgentState):

    def check_memory():
        if not os.path.exists("memory.json"):
            return False

        with open("memory.json", "r") as f:
            memory = json.load(f)

        if not memory:
            return False

        previous_queries = [memory[i]["query"] for i in memory]

        prompt = f"""
        You are a topic similarity detector.

        Current query: {state["query"]}
        Previous researched topics: {previous_queries}

        Is the current query about the same topic as any of the above?
        Reply with ONLY the exact matching topic from the list, or NONE if no match.
        """

        response = call_llm(prompt, "fast")
        match = response.strip()

        if match != "NONE" and match in memory:
            state["extracted_notes"] = memory[match]["notes"]
            state["memory_used"] = True
            print(f"\nMemory match found: '{match}'! Skipping search...")
            return True

        return False


    def plan_query():
        try:
            prompt = f"""
            You are a research query planner.

            SIMPLE: The query is about a single entity, person, place, or fact.
            COMPLEX: The query requires comparison, analysis, or research across multiple entities or topics.

            If COMPLEX, break this query into a maximum of 3 short, search-engine-friendly sub-queries.

            Query: "{state['query']}"

            Rules:
            - Each sub-query must be 3-6 words only
            - No full sentences or questions

            Respond ONLY in this JSON format:
            {{
                "complexity": "SIMPLE" or "COMPLEX",
                "sub_queries": []
            }}
            """

            response = call_llm(prompt, "fast")

            json_match = re.search(r"\{.*\}", response, re.DOTALL)

            if not json_match:
                raise ValueError("No JSON found in LLM response")

            result = json.loads(json_match.group())

            state["query_complexity"] = result.get("complexity", "SIMPLE")

            if state["query_complexity"] == "COMPLEX":
                state["sub_queries"] = result.get("sub_queries", [])
            else:
                state["sub_queries"] = [state["query"]]

        except Exception as e:
            print(f"Error in plan_query: {e}")

            # Fallback
            state["query_complexity"] = "SIMPLE"
            state["sub_queries"] = [state["query"]]

    try:
        if not check_memory():
            plan_query()
    except Exception as e:
        print(f"Error in planner_node: {e}")
        state["memory_used"] = False

    return state