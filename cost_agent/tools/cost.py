import os
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from google.adk.tools import ToolContext
from dotenv import load_dotenv
from typing import List

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
print("Connected to Qdrant Cloud successfully!")

embed_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
print("Loaded embedding model successfully!")

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("Error: QDRANT_URL or QDRANT_API_KEY not found in the .env file!")


def get_single_medication_price(query_name: str, tool_context: ToolContext) -> dict:
    """
    Takes the name of a drug (string) as input and returns the price information for that drug.
    """

    
    
    SIMILARITY_THRESHOLD = os.getenv("SIMILARITY_THRESHOLD", 0.5) 

    query_vector = embed_model.encode(query_name).tolist()

    try:
        response = qdrant_client.query_points(
            collection_name="medication_prices",
            query=query_vector, # Tham số đổi từ query_vector sang query
            limit=1
        )

        search_response = response.points

        if search_response and float(search_response[0].score) >= float(SIMILARITY_THRESHOLD):
            best_match = search_response[0]
            return {
                "requested_name": query_name,
                "matched_official_name": best_match.payload["official_name"],
                "unit_price_usd": best_match.payload["unit_price"],
                "similarity_score": round(best_match.score, 3),
                "status": "found"
            }
        
        else:
            score = round(search_response[0].score, 3) if search_response else 0
            return {
                "requested_name": query_name,
                "unit_price_usd": 0.0,
                "similarity_score": score,
                "status": "not_found"
            }

    except Exception as e:
        return {
            "requested_name": query_name,
            "unit_price_usd": 0.0,
            "status": "error",
            "error_detail": str(e)
        }

def calculate_total_prescription_cost(medications: List[dict], tool_context: ToolContext) -> dict:
    """
    Receive the list of medications (including quantities), call Function 1 to get the price of each item and calculate the total cost of the entire prescription.
    """
    
    if not medications:
        return {"status": "error", "message": "Empty medications."}
    
    total_cost_usd = 0.0
    detailed_results = []
    items_not_found = 0

    try:
        total_cost_usd = 0.0
        detailed_results = []
        items_not_found = 0

        for med in medications:
            query_name = med.get("name", "")
            
            try:
                quantity = float(med.get("quantity", 1))
            except ValueError:
                quantity = 1.0 # Mặc định là 1 nếu ép kiểu thất bại
        
            med_info = get_single_medication_price(query_name, tool_context)

            med_info["quantity"] = quantity

            if med_info.get("status") == "found":
                item_total = med_info["unit_price_usd"] * quantity
                med_info["item_total_usd"] = round(item_total, 2)
                total_cost_usd += item_total
            else:
                med_info["item_total_usd"] = 0.0
                items_not_found += 1
                
            detailed_results.append(med_info)
        
        return {
            "status": "success",
            "total_items_processed": len(medications),
            "items_not_found": items_not_found,
            "grand_total_usd": round(total_cost_usd, 2),
            "details": detailed_results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"An error occurred during calculation: {str(e)}"
        }



