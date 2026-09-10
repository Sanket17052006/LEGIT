# Legal Metrology Compliance Checker - ML Module

Standalone ML module for OCR extraction and field detection from product images.

## Status

🚧 **PLACEHOLDER** - This module is ready for ML team to implement.

## Goals

1. **OCR Text Extraction** - Extract all text from product images
2. **Field Detection** - Identify mandatory declaration fields
3. **Font Analysis** - Check font size and readability
4. **Label Detection** - Locate label positions on packaging

## Tech Stack (Planned)

- **OCR:** Tesseract / EasyOCR / PaddleOCR
- **Detection:** YOLO / Detectron2
- **Classification:** Custom CNN / ViT
- **Framework:** PyTorch / TensorFlow

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies (add when ready)
pip install -r requirements.txt
```

## Project Structure

```
ml/
├── models/               # Trained model files (.h5, .pt, .pkl)
├── data/                 # Training data and datasets
├── notebooks/            # Jupyter notebooks for experiments
├── scripts/              # Training and inference scripts
│   ├── train.py          # Model training script
│   ├── inference.py      # Inference script
│   └── preprocess.py     # Data preprocessing
├── ocr_engine.py         # OCR service implementation
├── field_detector.py     # Field detection module
├── font_analyzer.py      # Font size analysis
├── requirements.txt
└── README.md
```

## Integration with Backend

The backend's `ocr_service.py` is the integration point. 

### Option A: REST API
```python
# In backend/app/services/ocr_service.py
import httpx

async def extract_fields(image_path: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/extract",
            files={"file": open(image_path, "rb")}
        )
        return response.json()
```

### Option B: Direct Import
```python
# In backend/app/services/ocr_service.py
import sys
sys.path.append("../ml")
from ocr_engine import OCREngine

ocr = OCREngine()
def extract_fields(image_path: str) -> dict:
    return ocr.extract(image_path)
```

## API Endpoints (Planned)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/extract` | Extract text from image |
| POST | `/detect-fields` | Detect mandatory fields |
| POST | `/analyze-font` | Analyze font readability |
| GET | `/health` | Health check |

## Dataset Sources

- [Consumer Affairs Dataset](https://consumeraffairs.gov.in/pages/legal-metrology-act)
- Legal Metrology (Packaged Commodities) Rules, 2011
