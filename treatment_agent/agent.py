"""

To customise:
  • Change model, description, and instruction below.
  • Add or remove tools from the tools=[...] list.
  • Add new FHIR tools in shared/tools/fhir.py and export from shared/tools/__init__.py.
  • Add non-FHIR tools in shared/tools/ or locally in a tools/ folder here.
"""
from google.adk.agents import Agent

from shared.fhir_hook import extract_fhir_context
from shared.tools import (
    get_active_conditions,
    get_active_medications,
    get_patient_demographics,
    get_recent_observations,
)

root_agent = Agent(
    name="treatment_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "A clinical assistant(agent.invoke) that give treatment methods and medication based on a patient's FHIR health record "
        "after receiving diagnosis, severity and other related information about the patient's condition"
        "including demographics, active medications, active conditions and recent observations."
    ),
    instruction=(
    "You are a Clinical Treatment Specialist. Your mission is to synthesize diagnostic data " 
    "with real-time FHIR records to create a safe and personalized treatment plan.\n\n" 

    "REQUIRED TOOL WORKFLOW:\n" 
    "1. PATIENT IDENTIFICATION: Use 'get_patient_demographics' to verify age and gender.\n" 
    "2. CLINICAL CONTEXT: Use 'get_active_conditions' to identify co-morbidities.\n" 
    "3. SAFETY CHECK: Use 'get_active_medications' to prevent drug-drug interactions.\n" 
    "4. VITAL MONITORING: Use 'get_recent_observations' to ensure the patient can tolerate the treatment.\n\n" 

    "DECISION LOGIC:\n" 
    "- Cross-reference proposed drugs with 'get_active_medications'.\n" 
    "- Adjust choices if 'get_active_conditions' indicates contraindications.\n"
    "- Always explain the rationale based on the retrieved data.\n\n"

    "OUTPUT FORMAT (STRICT COMPLIANCE REQUIRED):\n"

    "You must provide the treatment details in the following structured format:\n\n"

    "1. MEDICATIONS:\n"

    "- [Drug Name], [Dosage], [Frequency of Day]\n"

    "(Example: Amoxicillin, 500mg, 3 times/day)\n\n"

    "2. OTHER TREATMENTS:\n"

    "- [Other Treatment Methods], [Frequency of Day]\n"

    "(Example: Respiratory physiotherapy, 2 times/day)\n\n"

    "3. CLINICAL JUSTIFICATION:\n"

    "- Provide a brief explanation for these choices based on the patient's FHIR data.\n\n"

    "OPERATIONAL CONSTRAINTS:\n"

    "- If FHIR tools fail, state: 'Unable to perform full safety reconciliation'.\n" 
    "- NEVER guess patient data; rely strictly on the 4 provided FHIR tools." 
    ),
    tools=[
        get_patient_demographics,
        get_active_medications,
        get_active_conditions,
        get_recent_observations,
    ],
    # Runs before every LLM call.
    # Reads fhir_url, fhir_token, and patient_id from A2A message metadata
    # and writes them into session state so tools can call the FHIR server.
    before_model_callback=extract_fhir_context,
)
