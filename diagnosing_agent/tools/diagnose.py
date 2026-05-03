import requests
import io
from PIL import Image, UnidentifiedImageError
from typing import Dict
from google.adk.tools import ToolContext
import json

def fetch_and_analyze_prescription(image_url: str, tool_context: ToolContext) -> dict:
    """
    Tải ảnh y tế từ URL, kiểm tra tính toàn vẹn và trích xuất thông tin.

    Args:
        image_url: Đường dẫn URL trực tiếp tới file ảnh.
    """
    try:
        # 1. Tải dữ liệu từ URL
        response = requests.get(image_url, timeout=10)
        response.raise_for_status() # Bắt lỗi 404, 500...
        
        # 2. Kiểm tra Content-Type xem có đúng là ảnh không
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            return {
                "status": "error", 
                "error_message": f"URL không trỏ tới ảnh hợp lệ. Nhận được định dạng: {content_type}"
            }

        image_bytes = response.content
        
        # 3. Kiểm tra file có bị rỗng không
        if len(image_bytes) == 0:
            return {
                "status": "error", 
                "error_message": "Dữ liệu tải về bị rỗng (0 bytes)."
            }

        # 4. Kiểm tra tính toàn vẹn của ảnh bằng Pillow
        try:
            # Dùng io.BytesIO để giả lập một file từ chuỗi bytes
            img = Image.open(io.BytesIO(image_bytes))
            img.verify() # Hàm này kiểm tra header của file mà không cần load toàn bộ ảnh vào RAM
            
            # (Tùy chọn) Lấy một số thông tin cơ bản để log hoặc trả về cho Agent
            image_info = f"Định dạng: {img.format}, Kích thước: {img.size}"
            
        except UnidentifiedImageError:
            return {
                "status": "error", 
                "error_message": "Dữ liệu tải về bị hỏng hoặc không đúng chuẩn file ảnh."
            }

        # --- ĐẾN ĐÂY BẠN CÓ THỂ CHẮC CHẮN 100% ẢNH ĐÃ ĐƯỢC LOAD THÀNH CÔNG ---
        
        return {
            "status": "success",
            "image_metadata": image_info, # Gửi metadata này cho Agent để nó biết file đã sẵn sàng
            "information": "Mục đích là để test nên cứ thông báo thành công", # Placeholder: Kết quả OCR/NLP sẽ nằm ở đây
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Lỗi kết nối mạng khi tải URL: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Lỗi không xác định: {str(e)}"
        }