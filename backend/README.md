# Legal Metrology Compliance Checker - Backend API

Standalone FastAPI backend for checking compliance of Packaged Commodities under Legal Metrology (Packaged Commodities) Rules, 2011.

## Tech Stack

- **Framework:** FastAPI 0.104.1
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **ORM:** SQLAlchemy 2.0
- **Auth:** JWT (python-jose)
- **Image Processing:** Pillow, OpenCV, Tesseract OCR

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy env file
cp .env.example .env

# Run server
uvicorn app.main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI application entry
│   ├── config.py         # Settings and env vars
│   ├── database.py       # DB connection
│   ├── models/
│   │   ├── models.py     # SQLAlchemy models
│   │   └── schemas.py    # Pydantic schemas
│   ├── routers/
│   │   ├── scans.py      # Scan CRUD endpoints
│   │   └── auth.py       # Auth endpoints
│   ├── services/
│   │   ├── compliance_checker.py   # Rule engine
│   │   ├── compliance_rules.py     # Legal Metrology rules
│   │   └── ocr_service.py          # OCR (ML integration point)
│   └── utils/
│       ├── auth.py       # JWT utilities
│       └── image.py      # Image utilities
├── uploads/              # Uploaded images (gitignored)
├── tests/                # Test files
├── requirements.txt
├── .env.example
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get token |
| GET | `/auth/users` | List all users |
| POST | `/scans/` | Create scan manually |
| POST | `/scans/upload` | Upload image and scan |
| GET | `/scans/` | List all scans |
| GET | `/scans/{id}` | Get scan with checks |
| GET | `/scans/stats/dashboard` | Dashboard statistics |
| DELETE | `/scans/{id}` | Delete a scan |

## Integration with ML Module

The OCR service (`services/ocr_service.py`) is the integration point for the ML module. When ML team implements their models:

1. Update `ocr_service.py` to call the ML service
2. ML service should expose REST endpoints or be importable
3. The compliance checker will use extracted fields from OCR

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./compliance_checker.db` |
| `SECRET_KEY` | JWT secret key | Change in production |
| `UPLOAD_DIR` | Upload directory path | `./uploads` |
| `MAX_FILE_SIZE` | Max upload size in bytes | `10485760` (10MB) |
| `ALLOWED_EXTENSIONS` | Allowed file types | `jpg,jpeg,png,webp` |
