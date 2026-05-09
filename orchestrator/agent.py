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
        "A comprehensive clinical orchestrator that manages the entire patient pipeline: "
        "from AI-driven image diagnostics to treatment planning, scheduling, and billing. "
        "It takes patient symptoms and medical image URLs to generate a preliminary diagnosis, "
        "a personalized treatment plan, a daily schedule, and an estimated prescription cost."
    ),
    instruction=(
        "You are a Clinical Orchestrator managing a full End-to-End clinical workflow. "
        "You must coordinate the diagnosing, treatment, scheduling, and billing processes. "
        "Follow these sequential steps strictly:\n\n"

        "STEP 1: DIAGNOSING (VLM ANALYSIS)\n"
        "- Check the user's prompt for a medical image URL and symptoms.\n"
        "- IF an image URL is MISSING: Politely pause the process and ask the user to provide one. "
        "Explicitly guide them by saying something like: 'If you don't have an image link, you can upload your medical photo to the website https://postimages.org/, "
        "then copy the Direct link and paste it here for the AI ​​system to analyze."
        "- Once the URL and symptoms are available, pass them to the 'diagnosing_agent' to get "
        "the 'diagnosis_result' (disease name) and 'severity'.\n\n"

        "STEP 2: TREATMENT & MEDICATION\n"
        "- Take the 'diagnosis_result' and 'severity' from Step 1.\n"
        "- Pass this information to 'treatment_agent' to get: Medication names, dosages, "
        "  frequencies, total quantities, and other therapeutic methods.\n"
        "- Ensure the 'treatment_agent' performs safety checks against the patient's FHIR records.\n\n"

        "STEP 3: SCHEDULING & VISUALIZATION\n"
        "- Take the medication list and treatment methods from Step 2 and pass them to 'scheduling_agent'.\n"
        "- The 'scheduling_agent' must return a structured, actionable daily calendar.\n\n"

        "STEP 4: COST ESTIMATION & BILLING\n"
        "- Extract the finalized list of medications and their TOTAL QUANTITIES from Step 2.\n"
        "- Pass this information to 'cost_agent' to calculate the estimated financial cost.\n"
        "- The 'cost_agent' will return a transparent, itemized receipt and the whole output of the list of medications including similarity score and status.\n\n"

        "FINAL OUTPUT RULE:\n"
        "- Combine all information from Step 1 to Step 4 into a professional, cohesive clinical report.\n"
        "- Clearly state the AI's preliminary diagnosis based on the image.\n"
        "- The final result MUST include a **Visualized/Markdown Table** representing the treatment schedule.\n"
        "- The final result MUST include the **Itemized Receipt (Markdown Table)** from the cost_agent.\n"
        "- Maintain a highly professional and empathetic tone throughout the report."
    ),
    tools=[
        AgentTool(agent=diagnosing_agent), 
        AgentTool(agent=treatment_agent),
        AgentTool(agent=scheduling_agent),
        AgentTool(agent=cost_agent),
    ],
    before_model_callback=extract_fhir_context,
)