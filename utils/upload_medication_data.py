import os
from dotenv import load_dotenv
# pip install qdrant-client sentence-transformers
import json
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("Lỗi: Không tìm thấy QDRANT_URL hoặc QDRANT_API_KEY trong file .env!")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
collection_name = "medication_prices"

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=384, # Kích thước vector của model all-MiniLM-L6-v2
        distance=Distance.COSINE
    ),
)

model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

try:
    with open('./data/medication.json', 'r', encoding='utf-8') as f:
        medications_db = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("Not found medication.json file. Please ensure it exists in the ./data/ directory.")

points = []

for item in medications_db:
    item_id = item["id"]
    payload_data = item["payload"]
    
    official_name = payload_data["name"]
    price = payload_data["price_per_unit"]
    variants = payload_data.get("name_variants", [])
    
    text_to_encode = f"{official_name} " + " ".join(variants)
    
    vector = model.encode(text_to_encode).tolist()
    
    point = PointStruct(
        id=item_id,
        vector=vector,
        payload={
            "official_name": official_name, 
            "unit_price": price
        }
    )
    points.append(point)

client.upsert(
    collection_name=collection_name, 
    points=points
)