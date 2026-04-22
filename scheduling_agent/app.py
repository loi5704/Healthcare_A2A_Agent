import os
from a2a.types import AgentSkill
from shared.app_factory import create_a2a_app
from .agent import root_agent

a2a_app = create_a2a_app(
    agent=root_agent,
    name="scheduling_agent",
    description=(
         "A clinical assistant that organizes medications and treatment methods "
        "into a structured daily schedule for the patient."
    ),
    url=os.getenv("SCHEDULING_AGENT_URL", "http://localhost:8006"),
    port=8006,
    require_api_key=False,
    skills=[
        AgentSkill(
            id="treatment-scheduling",
            name="treatment-scheduling",
            description="Create structured daily calendars for medications and clinical procedures.",
            tags=["scheduling", "planning", "patient-care"],
        ),
    ],
)