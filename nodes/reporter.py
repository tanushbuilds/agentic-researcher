import os
from openai import OpenAI
from dotenv import load_dotenv
from agent_state import AgentState

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def report_node(state: AgentState) -> AgentState:
    notes = "\n\n".join([state.get("extracted_notes", "")])

    try:
        prompt = f"""
        You are a professional long-form research writer.

        Write a comprehensive, deeply analytical research report in clean Markdown format.

        IMPORTANT FORMATTING RULES:
        - Use # for the main title
        - Use ## for major sections
        - Use ### for subsections
        - Use structured paragraphs (NOT excessive bullet points)
        - Output ONLY the final report in Markdown
        - Do NOT include commentary outside the report

        WRITING REQUIREMENTS:
        - The report must be expansive and detailed.
        - Each major section must contain multiple well-developed paragraphs.
        - Avoid short explanations.
        - Provide depth, interpretation, and contextual expansion.
        - Minimum target length: 1800–2500 words.

        Structure the report as follows:

        # Comprehensive Research Report Title

        ## Introduction
        Provide detailed background, historical context, relevance, and scope of the topic.
        Establish why the subject matters in a broader perspective.

        ## Historical and Contextual Background
        Explain origins, development, and evolution related to the topic.
        Include timeline-based progression where applicable.

        ## Key Findings and Core Themes
        For each major finding:
        - Create a ### Subsection heading
        - Provide at least 2–3 full paragraphs
        - Include explanation
        - Include reasoning
        - Include implications
        - Include examples or supporting detail

        ## In-Depth Analysis
        Provide deep interpretation and critical discussion.
        Include:
        - Connections between findings
        - Comparative perspectives
        - Strengths and limitations
        - Counterpoints where relevant
        - Broader industry or societal implications

        ## Practical Applications and Real-World Impact
        Explain how the findings translate into real-world outcomes.
        Discuss influence, strategy, or implementation where relevant.

        ## Future Outlook and Emerging Directions
        Discuss:
        - Trends
        - Unanswered questions
        - Long-term implications
        - Potential developments

        ## Conclusion
        Provide a strong, reflective, and well-developed closing synthesis.
        Do not summarize briefly — instead synthesize insights meaningfully.

        Research Notes:
        {notes}
        """

        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.75,
        )

        report = response.choices[0].message.content
        state["final_report"] = report

    except Exception as e:
        print(f"\nError in report_node: {e}")
        state["final_report"] = "Report generation failed."

    return state