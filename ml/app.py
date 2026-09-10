from fastapi import FastAPI, UploadFile, File
from ocr_engine import OCREngine, FieldDetector

app = FastAPI(title="ML Service", version="1.0.0")

ocr = OCREngine()
detector = FieldDetector()


@app.get("/health")
def health():
    return {"status": "healthy", "service": "ml"}


@app.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    """Extract text from uploaded image."""
    contents = await file.read()
    
    # Save temp file
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name
    
    try:
        result = ocr.extract(tmp_path)
        return result
    finally:
        os.unlink(tmp_path)


@app.post("/detect-fields")
async def detect_fields(file: UploadFile = File(...)):
    """Extract text and detect mandatory fields."""
    contents = await file.read()
    
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name
    
    try:
        text_result = ocr.extract(tmp_path)
        fields = detector.detect(text_result.get("raw_text", ""))
        return {
            "text": text_result,
            "fields": fields
        }
    finally:
        os.unlink(tmp_path)
