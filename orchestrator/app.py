"""
orchestrator — A2A application entry point.

Start the server with:
    uvicorn orchestrator.app:a2a_app --host 0.0.0.0 --port 8003

The agent card is served publicly at:
    GET http://localhost:8003/.well-known/agent-card.json

All other endpoints require an X-API-Key header (see shared/middleware.py).
"""
import os

from a2a.types import AgentSkill
from shared.app_factory import create_a2a_app

from .agent import root_agent

a2a_app = create_a2a_app(
    agent=root_agent,
    name="Clinical Orchestrator",
    description=(
        "A clinical orchestrator that manages treatment planning and scheduling. "
        "It takes a confirmed diagnosis and severity level as input to generate "
        "a personalized treatment plan and daily schedule."
    ),
    url=os.getenv("ORCHESTRATOR_URL", os.getenv("BASE_URL", "http://localhost:8003")),
    port=8003,
    
    # Giữ nguyên FHIR Extension để có thể nhận Token từ Prompt Opinion
    fhir_extension_uri=f"{os.getenv('PO_PLATFORM_BASE_URL', 'http://localhost:5139')}/schemas/a2a/v1/fhir-context",
    fhir_scopes=[
        {"name": "patient/Patient.rs",           "required": True},
        {"name": "patient/MedicationRequest.rs", "required": True},
        {"name": "patient/Condition.rs",         "required": True},
        {"name": "patient/Observation.rs",       "required": True},
    ],
    skills=[
        AgentSkill(
            id="clinical-workflow-orchestration",
            name="Clinical Workflow Orchestration",
            description="Coordinates multi-agent pipelines to process medical data from diagnosis to final treatment plans.",
            tags=["orchestration", "workflow", "clinical"],
        ),
        AgentSkill(
            id="treatment-planning-management",
            name="Treatment Planning & Management",
            description="Integrates specialist recommendations and FHIR records to formulate comprehensive treatment strategies.",
            tags=["planning", "treatment", "decision-support"],
        ),
        AgentSkill(
            id="daily-schedule-visualization",
            name="Daily Schedule Visualization",
            description="Converts clinical treatment plans into actionable, visualized daily calendars for patients.",
            tags=["scheduling", "visualization", "patient-care"],
        ),
    ],
)
