from typing import Optional
import httpx
import os
from app.config import settings


class OCRService:
    """
    OCR Service - connects to ML microservice for text extraction.
    Falls back to placeholder if ML service is unavailable.
    """

    def __init__(self):
        self.ml_service_url = os.getenv("ML_SERVICE_URL", "http://localhost:8001")

    async def extract_text(self, image_path: str) -> Optional[str]:
        """Extract text from image via ML service."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                with open(image_path, "rb") as f:
                    response = await client.post(
                        f"{self.ml_service_url}/extract",
                        files={"file": (os.path.basename(image_path), f, "image/jpeg")}
                    )
                if response.status_code == 200:
                    return response.json().get("raw_text", "")
        except Exception as e:
            print(f"ML service unavailable: {e}")

        return f"[OCR Placeholder] Text extraction from {image_path} - ML service offline"

    async def extract_fields(self, image_path: str) -> dict:
        """Extract specific fields from product image via ML service."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                with open(image_path, "rb") as f:
                    response = await client.post(
                        f"{self.ml_service_url}/detect-fields",
                        files={"file": (os.path.basename(image_path), f, "image/jpeg")}
                    )
                if response.status_code == 200:
                    data = response.json()
                    fields = data.get("fields", {})
                    fields["confidence"] = data.get("text", {}).get("confidence", 0.0)
                    fields["raw_text"] = data.get("text", {}).get("raw_text", "")
                    return fields
        except Exception as e:
            print(f"ML service unavailable: {e}")

        # Fallback when ML service is down
        raw_text = await self.extract_text(image_path)
        return {
            "manufacturer": None,
            "packer": None,
            "importer": None,
            "net_quantity": None,
            "mrp": None,
            "manufacture_date": None,
            "expiry_date": None,
            "consumer_care": None,
            "country_of_origin": None,
            "confidence": 0.0,
            "raw_text": raw_text
        }


ocr_service = OCRService()
