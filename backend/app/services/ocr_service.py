"""
OCR Service - Backend owns OCR + field detection.

Pipeline:
  1. Send image to ML service /preprocess for cropping (optional, ML pending)
  2. If cropped image returned, use it; else use original
  3. Run Tesseract OCR with multiple preprocessing strategies
  4. Run regex field detection on extracted text
  5. Return fields + raw text for compliance checking

When the ML team adds their cropping model, this service automatically
uses the cropped image. No backend changes needed.
"""

from typing import Optional
import re
import httpx
import os
import base64
import uuid
import tempfile
import pytesseract
import cv2
import numpy as np
from PIL import Image


class OCRService:
    """Extracts text and mandatory declaration fields from product images."""

    def __init__(self):
        self.ml_service_url = os.getenv("ML_SERVICE_URL", "http://localhost:8001")

    async def extract_fields(self, image_path: str) -> dict:
        """
        Full extraction pipeline: ML preprocess -> OCR -> field detection.

        Returns:
            dict with 9 declaration field values + raw_text
        """
        work_image = await self._preprocess_image(image_path)

        raw_text = self._extract_text_local(work_image)
        fields = self._detect_fields_from_text(raw_text)
        fields["raw_text"] = raw_text
        return fields

    async def _preprocess_image(self, image_path: str) -> str:
        """
        Call ML service /preprocess. Returns path to best image for OCR.

        If ML service is unavailable/returns invalid data, falls back to
        the original image so the pipeline keeps working.
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                with open(image_path, "rb") as f:
                    response = await client.post(
                        f"{self.ml_service_url}/preprocess",
                        files={"file": (os.path.basename(image_path), f, "image/jpeg")}
                    )
                if response.status_code == 200:
                    data = response.json()
                    image_b64 = data.get("image", "")
                    if image_b64:
                        cropped_bytes = base64.b64decode(image_b64)
                        if len(cropped_bytes) > 0 and cropped_bytes != self._file_bytes(image_path):
                            tmp_path = os.path.join(
                                tempfile.gettempdir(), f"preprocessed_{uuid.uuid4()}.jpg"
                            )
                            with open(tmp_path, "wb") as f:
                                f.write(cropped_bytes)
                            print(f"ML preprocessing applied, using cropped image: {tmp_path}")
                            return tmp_path
        except Exception as e:
            print(f"ML preprocess unavailable, using original image: {e}")

        return image_path

    def _file_bytes(self, path: str) -> bytes:
        with open(path, "rb") as f:
            return f.read()

    def _extract_text_local(self, image_path: str) -> str:
        """Extract text using local Tesseract OCR with multiple preprocessing attempts."""
        try:
            img = cv2.imread(image_path)
            if img is None:
                print(f"Could not read image: {image_path}")
                return ""

            results = []

            # Strategy 1: Adaptive threshold
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            processed = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10
            )
            processed = cv2.resize(processed, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            text1 = pytesseract.image_to_string(
                Image.fromarray(processed), config="--psm 6"
            ).strip()
            if text1:
                results.append(text1)

            # Strategy 2: OTSU threshold + denoise
            _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            denoised = cv2.fastNlMeansDenoising(otsu, h=10)
            denoised = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            text2 = pytesseract.image_to_string(
                Image.fromarray(denoised), config="--psm 6"
            ).strip()
            if text2:
                results.append(text2)

            # Strategy 3: Invert if dark background
            if np.mean(gray) < 127:
                inverted = cv2.bitwise_not(gray)
                _, inv_thresh = cv2.threshold(inverted, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                inv_thresh = cv2.resize(inv_thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                text3 = pytesseract.image_to_string(
                    Image.fromarray(inv_thresh), config="--psm 6"
                ).strip()
                if text3:
                    results.append(text3)

            # Strategy 4: Color image direct OCR
            resized_color = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            text4 = pytesseract.image_to_string(
                Image.fromarray(cv2.cvtColor(resized_color, cv2.COLOR_BGR2RGB)),
                config="--psm 6"
            ).strip()
            if text4:
                results.append(text4)

            if results:
                best = max(results, key=lambda t: len(t.split()))
                print(f"OCR extracted {len(best.split())} words")
                return best

            print("No text extracted from image")
            return ""
        except Exception as e:
            print(f"Local OCR failed: {e}")
            return ""

    SEPARATOR = r"[:\-\*.]"

    def _detect_fields_from_text(self, text: str) -> dict:
        """Detect mandatory declaration fields from OCR text using regex patterns."""
        if not text:
            return self._empty_fields()

        lines = text.split("\n")
        sep = self.SEPARATOR

        return {
            "manufacturer": self._find_field(lines, [
                rf"manufacturer\s*{sep}\s*(.+)",
                rf"mfr\s*{sep}\s*(.+)",
                rf"manufactured by\s*{sep}\s*(.+)",
                rf"packed by\s*{sep}\s*(.+)",
                rf"packed for\s*{sep}\s*(.+)",
                rf"marketed by\s*{sep}\s*(.+)",
                rf"produced by\s*{sep}\s*(.+)",
                rf"made by\s*{sep}\s*(.+)",
            ]),
            "packer": self._find_field(lines, [
                rf"packer\s*{sep}\s*(.+)",
                rf"packed by\s*{sep}\s*(.+)",
                rf"packed at\s*{sep}\s*(.+)",
            ]),
            "importer": self._find_field(lines, [
                rf"importer\s*{sep}\s*(.+)",
                rf"imported by\s*{sep}\s*(.+)",
                rf"imported & distributed by\s*{sep}\s*(.+)",
                rf"imported and distributed by\s*{sep}\s*(.+)",
            ]),
            "net_quantity": self._find_field(lines, [
                rf"net[\s.]*{sep}?\s*(?:qty|quantity|wt|weight|contents?)\s*{sep}\s*(.+)",
                rf"(?:net|quantity)\s*{sep}\s*(.+)",
                r"\b(\d+\.?\d*\s*(?:g|kg|ml|l|ltr|litre|grams?|kilograms?|millilitres?|litres?))\b",
            ]),
            "mrp": self._find_field(lines, [
                rf"mrp\s*{sep}?\s*(?:rs\.?|inr|\u20b9)?\s*(.+)",
                rf"maximum retail price\s*{sep}?\s*(?:rs\.?|inr|\u20b9)?\s*(.+)",
                rf"m\.?r\.?p\.?\s*{sep}?\s*(.+)",
                r"(?:rs\.?|inr|\u20b9)\s*(\d+\.?\d*)",
            ]),
            "manufacture_date": self._find_field(lines, [
                rf"m(?:fg|fgd|fd)?\.?\s*date\s*{sep}\s*(.+)",
                rf"manufactur(?:e|ing)\s*(?:date)?\s*{sep}\s*(.+)",
                rf"packed\s*(?:on|date)\s*{sep}\s*(.+)",
                rf"mfd\.?\s*(?:on|date)?\s*{sep}\s*(.+)",
                rf"date of manufacture\s*{sep}\s*(.+)",
                rf"(?:mfg|mfd)\.?\s*{sep}\s*(.+)",
            ]),
            "expiry_date": self._find_field(lines, [
                rf"exp(?:iry)?\.?\s*(?:date)?\s*{sep}\s*(.+)",
                rf"best before\s*{sep}\s*(.+)",
                rf"use by\s*{sep}\s*(.+)",
                rf"valid till\s*{sep}\s*(.+)",
                rf"date of expiry\s*{sep}\s*(.+)",
                rf"shelf life\s*{sep}\s*(.+)",
                rf"ex(?:p)?\.?\s*{sep}\s*(.+)",
            ]),
            "consumer_care": self._find_field(lines, [
                rf"consumer\s*care\s*{sep}\s*(.+)",
                rf"customer\s*care\s*{sep}\s*(.+)",
                rf"for\s*(?:queries|complaints|consumer)\s*{sep}\s*(.+)",
                rf"helpline\s*{sep}\s*(.+)",
                rf"contact\s*(?:us)?\s*{sep}\s*(.+)",
                rf"consumer\s*helpline\s*{sep}\s*(.+)",
            ]),
            "country_of_origin": self._find_field(lines, [
                rf"country\s*(?:of\s*)?origin\s*{sep}\s*(.+)",
                rf"origin\s*{sep}\s*(.+)",
                r"made in\s+(.+)",
                r"product of\s+(.+)",
                r"(?:manufactured|produced|made)\s+in\s+(.+)",
                rf"country\s+of\s+\w{{2,}}\s*{sep}\s*(.+)",
                r"(?i)country\s+of\s+(?:or[a-z]*|or[a-z]*n)\w*\s*[:\-\*\.]\s*(.+)",
            ]),
        }

    def _find_field(self, lines: list, patterns: list) -> Optional[str]:
        """Try multiple regex patterns against all lines to find a field value."""
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            for pattern in patterns:
                match = re.search(pattern, line_stripped, re.IGNORECASE)
                if match:
                    value = match.group(1).strip().rstrip("-").strip()
                    if value and len(value) > 1:
                        return value

        full_text = " ".join(lines)
        for pattern in patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                value = match.group(1).strip().rstrip("-").strip()
                if value and len(value) > 1:
                    return value

        return None

    def _empty_fields(self) -> dict:
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
        }


ocr_service = OCRService()