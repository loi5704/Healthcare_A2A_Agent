import os
from a2a.types import AgentSkill
from shared.app_factory import create_a2a_app
from .agent import root_agent

a2a_app = create_a2a_app(
    agent=root_agent,
    name="diagnosing_agent",
    description=(
        "A specialized clinical AI assistant equipped with a Vision-Language Model (VLM). "
        "It analyzes medical image URLs alongside patient symptoms to provide preliminary "
        "diagnostic insights, including disease identification and severity assessment."
    ),
    url=os.getenv("DIAGNOSING_AGENT_URL", "http://localhost:8007"),
    port=8007,
    require_api_key=False,
    skills=[
        AgentSkill(
            id="vlm-medical-diagnosis",
            name="VLM Medical Diagnosis",
            description="Analyzes medical image URLs in conjunction with patient symptoms to provide preliminary disease identification and severity assessment using a Vision-Language Model.",
            tags=["medical-imaging", "vlm", "diagnosis", "vision", "clinical"],
        ),
    ],
)