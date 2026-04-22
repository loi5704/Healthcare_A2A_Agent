import logging
from datetime import datetime, timedelta
from typing import List
from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

def create_treatment_schedule(medications: List[dict], treatment_plan: str, tool_context: ToolContext) -> dict:
    """
    Create a detailed daily schedule for medications and other clinical treatments.

    Args:
        medications: A list of medication objects. Each object must contain 
                     'name' (str), 'dosage' (str), and 'frequency' (str).
                     Example: [{"name": "Amoxicillin", "dosage": "500mg", "frequency": "3 times/day"}]
        treatment_plan: The overall non-pharmacological treatment strategy.
    """

    schedule = []

    time_slots = {
        "Morning": "08:00 AM",
        "Afternoon": "02:00 PM",
        "Evening": "08:00 PM"
    }

    for med in medications:
        name = med.get("name", "Unknown")
        freq = med.get("frequency", "1 time/day").lower()
        
        # Logic phân bổ dựa trên tần suất
        if "3 times" in freq:
            slots = ["Morning", "Afternoon", "Evening"]
        elif "2 times" in freq:
            slots = ["Morning", "Evening"]
        else:
            slots = ["Morning"]
            
        for slot in slots:
            schedule.append({
                "time": time_slots[slot],
                "medication": name,
                "dosage": med.get("dosage", ""),
                "action": "Take medication"
            })

    if schedule:
        return {
            "status": "success",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "daily_schedule": sorted(schedule, key=lambda x: x['time']),
            "general_advice": treatment_plan
        }
    else:
        return {
            "status": "error",
            "error_message": "No medications provided to create a schedule."
        }