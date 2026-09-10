# ML Service - Crop & Preprocess

This service crops scanned product images to essential label sections.
The backend calls this service, then runs OCR + compliance check on the
cropped image(s).

## Current Status

`/preprocess` returns the original image unchanged (pass-through).
The pipeline works end-to-end; no cropping is applied yet.

## ML Team: How to integrate

1. Build a **Jupyter notebook** that takes a scanned product image and
   returns cropped essential-section images (manufacturer block, MRP block,
   dates block, etc).
2. Export your cropping logic/model as a Python module, e.g. `crop_model.py`.
3. Wire it into `app.py` `/preprocess`:

```python
from crop_model import crop_to_sections

@app.post("/preprocess")
async def preprocess(file: UploadFile = File(...)):
    # ... save temp file ...
    sections = crop_to_sections(tmp_path)
    # returns {"image": <base64 cropped>, "cropped_regions": [...]}
```

4. Keep the response contract the same so the backend doesn't change.

## API Contract

| Method | Endpoint       | Purpose                                              |
|--------|----------------|------------------------------------------------------|
| GET    | /health        | Health check                                         |
| POST   | /preprocess    | Crop image to essential sections (returns base64 image + region metadata) |

## Pipeline (full flow)

```
Frontend uploads image
  -> Backend saves & validates image
  -> POST /preprocess (this service) -> cropped image
  -> Backend OCR (Tesseract) on cropped image
  -> Backend field detection (regex)
  -> Backend compliance check (Legal Metrology Rules)
  -> Backend returns results to frontend
```

## Notebooks

Put your Jupyter notebooks in `notebooks/`.
Model artifacts go in `models/`.
Datasets go in `data/`.
Training/preprocessing scripts go in `scripts/`.