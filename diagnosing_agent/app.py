import os
from a2a.types import AgentSkill
from shared.app_factory import create_a2a_app
from .agent import root_agent

a2a_app = create_a2a_app(
    agent=root_agent,
    name="diagnosing_agent",
    description=(
        "An AI assistant specialized in downloading images from URLs and "
        "extracting basic technical metadata, specifically the image format and size."
    ),
    url=os.getenv("DIAGNOSING_AGENT_URL", "http://localhost:8007"),
    port=8007,
    require_api_key=False,
    skills=[
        AgentSkill(
            id="image-metadata-extraction",
            name="image-metadata-extraction",
            description="Downloads images from URLs and extracts basic technical metadata (format, dimensions) to ensure file integrity.",
            tags=["image-processing", "metadata", "vision", "utility"],
        ),
    ],
)