import os
from dotenv import load_dotenv
# pip install qdrant-client sentence-transformers
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("Lỗi: Không tìm thấy QDRANT_URL hoặc QDRANT_API_KEY trong file .env!")

print("Đang kết nối tới Qdrant Cloud...")
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
collection_name = "medication_prices"

print(f"Đang thiết lập Collection '{collection_name}'...")
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=384, # Kích thước vector của model all-MiniLM-L6-v2
        distance=Distance.COSINE
    ),
)

print("Đang tải mô hình AI tạo vector...")
model = SentenceTransformer('all-MiniLM-L6-v2')

medications_db = [
    {"id": 1, "name": "Amoxicillin 500mg", "price_usd": 0.45},
    {"id": 2, "name": "Paracetamol 500mg", "price_usd": 0.15},
    {"id": 3, "name": "Ibuprofen 400mg", "price_usd": 0.25},
    {"id": 4, "name": "Omeprazole 20mg", "price_usd": 0.60},
    {"id": 5, "name": "Cetirizine 10mg", "price_usd": 0.30},
    {"id": 6, "name": "Vitamin C 1000mg", "price_usd": 0.20},
]

print("Đang mã hóa và đẩy dữ liệu lên Cloud...")
points = []
for med in medications_db:
    # Biến đổi tên thuốc thành dãy số (vector)
    vector = model.encode(med["name"]).tolist()
    
    # Đóng gói dữ liệu
    point = PointStruct(
        id=med["id"],
        vector=vector,
        payload={
            "official_name": med["name"], 
            "unit_price": med["price_usd"]
        }
    )
    points.append(point)

client.upsert(
    collection_name=collection_name, 
    points=points
)

print("✅ Đã nạp thành công dữ liệu giá thuốc lên Qdrant Cloud!")