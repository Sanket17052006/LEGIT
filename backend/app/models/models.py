from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    INSPECTOR = "inspector"
    ADMIN = "admin"
    VIEWER = "viewer"


class ComplianceStatus(str, enum.Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIAL = "partial"
    PENDING = "pending"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default=UserRole.INSPECTOR)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    scans = relationship("Scan", back_populates="user")


class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_path = Column(String)
    product_name = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)
    packer = Column(String, nullable=True)
    importer = Column(String, nullable=True)
    net_quantity = Column(String, nullable=True)
    mrp = Column(String, nullable=True)
    manufacture_date = Column(String, nullable=True)
    expiry_date = Column(String, nullable=True)
    consumer_care = Column(String, nullable=True)
    country_of_origin = Column(String, nullable=True)
    compliance_status = Column(String, default=ComplianceStatus.PENDING)
    violations = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="scans")
    checks = relationship("ComplianceCheck", back_populates="scan")


class ComplianceCheck(Base):
    __tablename__ = "compliance_checks"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    rule_id = Column(String)
    rule_name = Column(String)
    is_compliant = Column(Boolean)
    details = Column(Text, nullable=True)
    severity = Column(String)  # "error", "warning", "info"
    created_at = Column(DateTime, default=datetime.utcnow)

    scan = relationship("Scan", back_populates="checks")
