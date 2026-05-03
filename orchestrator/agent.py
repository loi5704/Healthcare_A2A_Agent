"""
orchestrator — Multi-agent orchestrator.

This agent delegates to specialist sub-agents using ADK's AgentTool.
Gemini decides which sub-agent to call based on the question.

Sub-agents run in-process (same Python process, not separate HTTP calls).
Session state is shared, so FHIR credentials extracted by this agent's
before_model_callback are available to the healthcare sub-agent's tools.

Sub-agents registered:
  healthcare_fhir_agent  — patient demographics, medications, conditions, observations
  general_agent          — date/time queries, ICD-10 code lookups

To add another sub-agent:
  1. Create a new agent package (copy healthcare_agent or general_agent as a template).
  2. Import its root_agent here.
  3. Add AgentTool(agent=your_new_agent) to the tools list.
  4. Update the instruction to describe when to use it.
"""
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from treatment_agent.agent import root_agent as treatment_agent
from scheduling_agent.agent import root_agent as scheduling_agent
from diagnosing_agent.agent import root_agent as diagnosing_agent
from cost_agent.agent import root_agent as cost_agent
from shared.fhir_hook import extract_fhir_context

root_agent = Agent(
    name="orchestrator",
    model="gemini-3.1-flash-lite-preview", 
    description=(
        "A clinical orchestrator that manages treatment planning, scheduling, and billing. "
        "It takes a confirmed diagnosis and severity level as input to generate "
        "a personalized treatment plan, daily schedule, and estimated prescription cost."
    ),
    instruction=(
        "You are a Clinical Orchestrator. Your role is to coordinate the treatment, "
        "scheduling, and billing workflow based on a confirmed diagnosis. Follow these steps:\n\n"

        "STEP 1: TREATMENT & MEDICATION\n"
        "- Receive the 'diagnosis' and 'severity level' directly from the user's prompt.\n"
        "- Pass this information to 'treatment_agent' to get: Medication names, dosages, "
        "  frequencies, total quantities, and other therapeutic methods.\n"
        "- Ensure the 'treatment_agent' performs safety checks against the patient's FHIR records.\n\n"

        "STEP 2: SCHEDULING & VISUALIZATION\n"
        "- Take the medication list and treatment methods from Step 1 and pass them to 'scheduling_agent'.\n"
        "- The 'scheduling_agent' must return a structured, actionable daily calendar.\n\n"

        "STEP 3: COST ESTIMATION & BILLING\n"
        "- Extract the finalized list of medications and their TOTAL QUANTITIES from Step 1.\n"
        "- Pass this information to 'cost_agent' to calculate the estimated financial cost.\n"
        "- The 'cost_agent' will return a transparent, itemized receipt.\n\n"

        "FINAL OUTPUT RULE:\n"
        "- Combine all information into a professional clinical report.\n"
        "- The final result MUST include a **Visualized/Markdown Table** representing the treatment schedule.\n"
        "- The final result MUST include the **Itemized Receipt (Markdown Table)** from the cost_agent.\n"
        "- If the user has not provided a clear diagnosis in their prompt, politely ask them "
        "  to provide the disease name and severity to begin the process.\n\n"
        "OTHER:\n"
        "If received input includes image URLs, call the diagnosing_agent to analyze and extract metadata and return output to user."
    ),
    tools=[
        AgentTool(agent=treatment_agent),
        AgentTool(agent=scheduling_agent),
        AgentTool(agent=cost_agent),
        AgentTool(agent=diagnosing_agent),
    ],
    before_model_callback=extract_fhir_context,
)