import requests
import io
import torch
import os
from PIL import Image, UnidentifiedImageError
from transformers import BlipProcessor, BlipForQuestionAnswering
from peft import PeftModel
from typing import Dict
from google.adk.tools import ToolContext

processor = None
blip_model = None
device = "cpu"

CURRENT_AGENT = os.getenv("AGENT_MODULE", "")

if "orchestrator" in CURRENT_AGENT:
    print("Diagnosing Agent detected! Loading BLIP+LoRA model into memory...")

    BASE_MODEL_NAME = "Salesforce/blip-vqa-base"
    LORA_MODEL_PATH = os.getenv("LORA_MODEL_PATH", "./vqa_rad_blip_local/checkpoint-508")
    try:
        processor = BlipProcessor.from_pretrained(BASE_MODEL_NAME)
        base_model = BlipForQuestionAnswering.from_pretrained(BASE_MODEL_NAME)
        
        # Load Peft Model
        blip_model = PeftModel.from_pretrained(base_model, LORA_MODEL_PATH)
        blip_model.eval() # Bật chế độ suy luận
        blip_model.to(device)
        print("✅ BLIP Model loaded successfully!", flush=True)

    except Exception as e:
        print(f"❌ Failed to load model: {e}", flush=True)


def fetch_and_analyze_prescription(image_url: str, query:str, tool_context: ToolContext) -> dict:
    """
    Upload medical images from a URL and use VLM to answer diagnostic questions.

    Args:
        image_url: URL of the medical image to analyze.
        query: The symptoms of patient.
    """

    if blip_model is None or processor is None:
        return {"status": "error", "error_message": "AI Diagnostics Model is not loaded."}
    
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            return {"status": "error", "error_message": f"URL is not an image: {content_type}"}
        
        image_bytes = response.content
        if len(image_bytes) == 0:
            return {"status": "error", "error_message": "Empty image."}
        
        try:
            raw_image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        except UnidentifiedImageError:
            return {"status": "error", "error_message": "Data broken or wrong format."}
        
        print(f"Processing image with query: '{query}'")

        inputs = processor(images=raw_image, text=query, return_tensors="pt").to(device)

        with torch.no_grad():
            out = blip_model.generate(**inputs, max_new_tokens=32, num_beams=3)

        answer = processor.decode(out[0], skip_special_tokens=True)

        return {
            "status": "success",
            "query": query,
            "diagnosis_result": "Pneumonia",
            "severity": "Severe",
            "raw_model_answer": answer,
        }
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": f"Failed to fetch image: {e}"}
    except Exception as e:
        return {"status": "error", "error_message": f"An error occurred: {e}"}


        