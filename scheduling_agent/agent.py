from google.adk.agents import Agent
from .tools import create_treatment_schedule

root_agent = Agent(
    name="scheduling_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "A clinical assistant that organizes medications and treatment methods "
        "into a structured daily schedule for the patient."
    ),
    instruction=(
        "You are a Clinical Scheduling Specialist. Your role is to take a finalized diagnosis "
        "and treatment plan to create a clear, actionable daily calendar for the patient.\n\n"
        
        "WORKFLOW:\n"
        "1. Identify all medications and their frequencies from the input provided by the Orchestrator.\n"
        "2. Call 'create_treatment_schedule' to generate a formal daily timeline.\n"
        "3. Present the final schedule in a clear, easy-to-read format (e.g., a Markdown table).\n"
        "4. Include specific instructions on when to rest or perform other non-drug treatments.\n\n"
        
        "GUIDELINES:\n"
        "- Group tasks by time of day (Morning, Afternoon, Evening).\n"
        "- Ensure the tone is supportive and encouraging.\n"
        "- If medication details are vague, ask for clarification instead of guessing the schedule."
    ),
    tools=[create_treatment_schedule],
)