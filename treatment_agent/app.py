"""
healthcare_agent — A2A application entry point.

Start the server with:
    uvicorn treatment_agent.app:a2a_app --host 0.0.0.0 --port 8005

The agent card is served publicly at:
    GET http://localhost:8005/.well-known/agent-card.json

All other endpoints require an X-API-Key header (see shared/middleware.py).
"""
import os

from a2a.types import AgentSkill
from shared.app_factory import create_a2a_app

from .agent import root_agent

print(os.getenv('PO_PLATFORM_BASE_URL'))

a2a_app = create_a2a_app(
    agent=root_agent,
    name="treatment_agent",
    description=(
        "A clinical assistant(agent.invoke) that give treatment methods and medication based on a patient's FHIR health record "
        "after receiving diagnosis, severity and other related information about the patient's condition"
        "including demographics, active medications, active conditions and recent observations."
    ),
    url=os.getenv("TREATMENT_AGENT_URL", os.getenv("BASE_URL", "http://localhost:8005")),
    port=8005,
    # This URI is the key under which callers send FHIR credentials in the
    # A2A message metadata.  Update to match your Prompt Opinion workspace URL.
    fhir_extension_uri=f"{os.getenv('PO_PLATFORM_BASE_URL', 'http://localhost:5139')}/schemas/a2a/v1/fhir-context",
    # SMART-on-FHIR scopes — one per FHIR resource type accessed by the tools.
    # All are marked required because each tool will fail without its scope.
    fhir_scopes=[
        {"name": "patient/Patient.rs",           "required": True},   # get_patient_demographics
        {"name": "patient/MedicationRequest.rs", "required": True},   # get_active_medications
        {"name": "patient/Condition.rs",         "required": True},   # get_active_conditions
        {"name": "patient/Observation.rs",       "required": True},   # get_recent_observations
    ],
    skills=[
        AgentSkill(
            id="treatment-recommendation",
            name="treatment-recommendation",
            description="Generate personalized treatment methods and precise medication plans based on diagnosis and patient context.",
            tags=["clinical", "treatment", "planning"],
        ),
        AgentSkill(
            id="patient-demographics",
            name="patient-demographics",
            description="Retrieve patient demographics like name, DOB, and contacts.",
            tags=["demographics", "fhir"],
        ),
        AgentSkill(
            id="active-medications",
            name="active-medications",
            description="Get a list of the patient's active medications and dosages.",
            tags=["medications", "fhir"],
        ),
        AgentSkill(
            id="active-conditions",
            name="active-conditions",
            description="Get the patient's active conditions and diagnoses.",
            tags=["conditions", "fhir"],
        ),
        AgentSkill(
            id="recent-observations",
            name="recent-observations",
            description="Retrieve recent vitals, lab results, and social history.",
            tags=["observations", "fhir"],
        ),
    ],
)
