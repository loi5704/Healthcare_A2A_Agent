from google.adk.agents import Agent
from .tools import fetch_and_analyze_prescription

root_agent = Agent(
    name="diagnosing_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "An AI assistant specialized in downloading images from URLs and "
        "extracting basic technical metadata, specifically the image format and size."
    ),
    instruction=(
        "You are a Technical Image Assistant. Your primary task is to retrieve "
        "and report the technical specifications of an image provided via a URL.\n\n"
        
        "WORKFLOW:\n"
        "1. When a user provides an image URL, immediately call the 'fetch_and_analyze_prescription' tool.\n"
        "2. Analyze the tool's JSON response.\n"
        "3. If the status is 'success', extract the 'image_metadata' field. Reply to the user by clearly stating the image's format (e.g., JPEG, PNG) and size (dimensions).\n"
        "4. If the status is 'error', politely inform the user of the exact 'error_message' provided by the tool.\n\n"
        
        "GUIDELINES:\n"
        "- Only report the format and size based on the tool's output. Do not guess or hallucinate details.\n"
        "- Keep your response concise, professional, and directly address the technical specs."
    ),
    tools=[fetch_and_analyze_prescription],
)