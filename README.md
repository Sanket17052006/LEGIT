# LEGIT - Legal Metrology Compliance Checker

Software System to check compliance of Packaged Commodities under Legal Metrology (Packaged Commodities) Rules, 2011 by scanning products, images and labels.

## Problem Statement

**ID:** 26034  
**Organization:** Ministry of Consumer Affairs, Food & Public Distribution  
**Department:** Department of Consumer Affairs (DoCA)

### Background

Packaged commodities are widely sold through retail stores, supermarkets and e-commerce platforms across India. Under the Legal Metrology Act, 2009 and the Legal Metrology (Packaged Commodities) Rules, 2011, every packaged commodity is required to bear mandatory declarations. This system automates compliance checking.

## Project Structure

```
LEGIT/
├── backend/          # FastAPI REST API (Standalone)
├── frontend/         # React Web Application (Standalone)
├── ml/               # ML Models & OCR (Standalone)
├── docker-compose.yml
└── README.md
```

Each module has its own `README.md`, `requirements.txt`, and can be developed independently.

## Quick Start (Docker)

```bash
# Clone the repo
git clone https://github.com/Sanket17052006/LEGIT.git
cd LEGIT

# Run everything with one command
docker-compose up --build
```

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Backend Docs:** http://localhost:8000/docs
- **ML Service:** http://localhost:8001

To stop: `docker-compose down`

## Quick Start (Without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### ML Module

```bash
cd ml
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How It Works

1. **Scan Product** - Upload or capture a product image
2. **ML Service** - Extracts text and detects mandatory fields (OCR)
3. **Backend** - Runs compliance rules against extracted data
4. **Results** - View pass/fail for each Legal Metrology rule

### Services Communication

```
Frontend (3000) --> Backend (8000) --> ML Service (8001)
```

- Frontend sends images to Backend via `/api/scans/upload`
- Backend calls ML Service to extract text and fields
- Backend runs compliance rules and returns results

## Features

- **Image Upload & Live Camera** - Upload or capture product images
- **Automated Compliance Checking** - Rule-based validation against Legal Metrology Rules 2011
- **Mandatory Declaration Detection** - Manufacturer, MRP, Net Quantity, Dates, etc.
- **Compliance Reports** - Pass/Fail for each rule with severity levels
- **Dashboard** - Statistics and enforcement monitoring
- **Scan History** - Repository of all scanned products
- **Role-Based Access** - Inspector, Admin, Viewer roles

## Mandatory Declarations Checked

| Rule | Declaration |
|------|-------------|
| LM-001 | Manufacturer/Packer/Importer Name & Address |
| LM-002 | Net Quantity Declaration |
| LM-003 | MRP Declaration |
| LM-004 | Manufacture/Packing Date |
| LM-005 | Consumer Care Details |
| LM-006 | Country of Origin |
| LM-007 | Expiry/Best Before Date |
| LM-008 | MRP Inclusive of All Taxes |
| LM-009 | Unit Price Declaration |
| LM-010 | Vegetarian/Non-Vegetarian Logo |

## Tech Stack

| Module | Technologies |
|--------|-------------|
| **Frontend** | React 18, Vite, Tailwind CSS, React Router |
| **Backend** | FastAPI, SQLAlchemy, SQLite, JWT Auth |
| **ML** | OpenCV, Tesseract/EasyOCR, PyTorch (planned) |
| **DevOps** | Docker, Docker Compose, Nginx |

## Team Roles

- **Frontend Team** - `frontend/` directory
- **Backend Team** - `backend/` directory  
- **ML Team** - `ml/` directory

## API Reference

See [Backend README](backend/README.md) for complete API documentation.

## Dataset

- [Consumer Affairs - Legal Metrology Act](https://consumeraffairs.gov.in/pages/legal-metrology-act)
- Legal Metrology (Packaged Commodities) Rules, 2011

## License

MIT
