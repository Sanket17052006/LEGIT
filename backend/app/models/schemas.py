from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class ScanBase(BaseModel):
    product_name: Optional[str] = None
    manufacturer: Optional[str] = None
    packer: Optional[str] = None
    importer: Optional[str] = None
    net_quantity: Optional[str] = None
    mrp: Optional[str] = None
    manufacture_date: Optional[str] = None
    expiry_date: Optional[str] = None
    consumer_care: Optional[str] = None
    country_of_origin: Optional[str] = None


class ScanCreate(ScanBase):
    raw_text: Optional[str] = None


class ScanResponse(ScanBase):
    id: int
    user_id: Optional[int] = None
    image_path: str
    compliance_status: str
    violations: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ComplianceCheckResponse(BaseModel):
    id: int
    scan_id: int
    rule_id: str
    rule_name: str
    is_compliant: bool
    details: Optional[str] = None
    severity: str
    created_at: datetime

    class Config:
        from_attributes = True


class ScanWithChecks(ScanResponse):
    checks: List[ComplianceCheckResponse] = []


class DashboardStats(BaseModel):
    total_scans: int
    compliant_count: int
    non_compliant_count: int
    pending_count: int
    recent_scans: List[ScanResponse]
