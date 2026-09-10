"""
ML Service - Legal Metrology Compliance Checker

PIPELINE CONTRACT:
  Frontend sends scan image -> Backend stores & saves it
  -> Backend calls POST /preprocess (THIS SERVICE)
  -> This service (ML team) crops/segments image to essential label sections
  -> Returns cropped image(s)
  -> Backend runs OCR on cropped image, extracts fields
  -> Backend runs compliance check
  -> Backend returns result to frontend

HOW ML TEAM INTEGRATES:
  1. Build your Jupyter notebook that takes a scanned image
     and returns cropped essential-section images.
  2. Export your cropping model/logic as a Python module.
  3. Import it in this file and wire it into the /preprocess endpoint below.
  4. That's it - the backend already calls this endpoint and handles
     OCR + compliance checking on whatever image you return.

Current state:
  /preprocess returns the original image unchanged (no cropping yet).
  This is intentional so the pipeline works end-to-end while the ML
  model is being built.
"""

from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="ML Service", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "healthy", "service": "ml"}


@app.post("/preprocess")
async def preprocess(file: UploadFile = File(...)):
    """
    Preprocess image: crop to essential label sections.

    Returns:
      {
        "image": base64-encoded cropped image,
        "cropped_regions": [region metadata],
        "preprocessing_applied": "description"
      }

    ML TEAM TODO: Implement real cropping here using your notebook model.
    Currently returns the original image unchanged so the pipeline works.
    """
    import tempfile
    import os
    import base64

    contents = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        return {
            "image": image_data,
            "filename": file.filename,
            "cropped_regions": [],
            "preprocessing_applied": "none - ML preprocessing pending",
        }
    finally:
        os.unlink(tmp_path)