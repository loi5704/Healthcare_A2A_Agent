import os
from a2a.types import AgentSkill
from shared.app_factory import create_a2a_app
from .agent import root_agent

a2a_app = create_a2a_app(
    agent=root_agent,
    name="cost_agent",
    description=(
        "A financial and medical billing assistant. It calculates the estimated total cost "
        "of a patient's prescription and provides a transparent, itemized receipt."
    ),
    url=os.getenv("COST_AGENT_URL", "http://localhost:8008"),
    port=8008,
    require_api_key=False,
    skills=[
        AgentSkill(
            id="prescription-cost-calculation",
            name="prescription-cost-calculation",
            description="Search medication prices via RAG and calculate the total estimated cost for a patient's prescription.",
            tags=["billing", "pricing", "cost-calculation", "pharmacy-receipt"],
        ),
    ],
)