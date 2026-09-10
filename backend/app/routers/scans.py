from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import Scan, ComplianceCheck, User
from app.models.schemas import ScanCreate, ScanResponse, ScanWithChecks, ComplianceCheckResponse
from app.services.compliance_checker import compliance_checker
from app.services.ocr_service import ocr_service
from app.utils.image import allowed_file, validate_image
from app.config import settings
import os
import shutil
import uuid

router = APIRouter(prefix="/scans", tags=["scans"])


@router.post("/", response_model=ScanResponse)
async def create_scan(
    scan: ScanCreate,
    db: Session = Depends(get_db)
):
    """Create a new scan with provided product data."""
    db_scan = Scan(**scan.model_dump())
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan


@router.post("/upload", response_model=ScanWithChecks)
async def upload_and_scan(
    file: UploadFile = File(...),
    product_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Upload product image, extract fields via ML, and run compliance check."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}"
        )

    # Save uploaded file
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_ext = file.filename.rsplit(".", 1)[1].lower()
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Validate image
    if not validate_image(file_path):
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Extract fields from image via ML service
    extracted_fields = await ocr_service.extract_fields(file_path)

    # Create scan record with extracted data
    db_scan = Scan(
        image_path=file_path,
        product_name=product_name or extracted_fields.get("product_name"),
        manufacturer=extracted_fields.get("manufacturer"),
        packer=extracted_fields.get("packer"),
        importer=extracted_fields.get("importer"),
        net_quantity=extracted_fields.get("net_quantity"),
        mrp=extracted_fields.get("mrp"),
        manufacture_date=extracted_fields.get("manufacture_date"),
        expiry_date=extracted_fields.get("expiry_date"),
        consumer_care=extracted_fields.get("consumer_care"),
        country_of_origin=extracted_fields.get("country_of_origin"),
    )
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)

    # Run compliance check with extracted data
    scan_data = ScanCreate(**{k: v for k, v in extracted_fields.items() if k in ScanCreate.model_fields})
    scan_data.raw_text = extracted_fields.get("raw_text", "")
    result = compliance_checker.check_compliance(scan_data)

    # Save compliance checks
    for check in result["checks"]:
        db_check = ComplianceCheck(
            scan_id=db_scan.id,
            rule_id=check["rule_id"],
            rule_name=check["rule_name"],
            is_compliant=check["is_compliant"],
            details=check["details"],
            severity=check["severity"]
        )
        db.add(db_check)

    # Update scan with compliance status
    db_scan.compliance_status = result["status"]
    db_scan.violations = str([v["rule_id"] for v in result["violations"]]) if result["violations"] else None

    db.commit()
    db.refresh(db_scan)

    # Fetch checks
    checks = db.query(ComplianceCheck).filter(ComplianceCheck.scan_id == db_scan.id).all()
    
    response = ScanWithChecks.model_validate(db_scan)
    response.checks = [ComplianceCheckResponse.model_validate(c) for c in checks]
    
    return response


@router.get("/", response_model=List[ScanResponse])
def list_scans(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all scans with optional filtering."""
    query = db.query(Scan)
    if status:
        query = query.filter(Scan.compliance_status == status)
    return query.offset(skip).limit(limit).all()


@router.get("/stats/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics."""
    total = db.query(Scan).count()
    compliant = db.query(Scan).filter(Scan.compliance_status == "compliant").count()
    non_compliant = db.query(Scan).filter(Scan.compliance_status == "non_compliant").count()
    pending = db.query(Scan).filter(Scan.compliance_status == "pending").count()
    recent = db.query(Scan).order_by(Scan.created_at.desc()).limit(10).all()

    return {
        "total_scans": total,
        "compliant_count": compliant,
        "non_compliant_count": non_compliant,
        "pending_count": pending,
        "recent_scans": [ScanResponse.model_validate(s) for s in recent]
    }


@router.get("/{scan_id}", response_model=ScanWithChecks)
def get_scan(scan_id: int, db: Session = Depends(get_db)):
    """Get a specific scan with its compliance checks."""
    db_scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not db_scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    checks = db.query(ComplianceCheck).filter(ComplianceCheck.scan_id == scan_id).all()
    response = ScanWithChecks.model_validate(db_scan)
    response.checks = [ComplianceCheckResponse.model_validate(c) for c in checks]
    return response


@router.delete("/{scan_id}")
def delete_scan(scan_id: int, db: Session = Depends(get_db)):
    """Delete a scan and its associated checks."""
    db_scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not db_scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    # Delete image file
    if os.path.exists(db_scan.image_path):
        os.remove(db_scan.image_path)
    
    # Delete checks
    db.query(ComplianceCheck).filter(ComplianceCheck.scan_id == scan_id).delete()
    db.delete(db_scan)
    db.commit()
    return {"message": "Scan deleted successfully"}
