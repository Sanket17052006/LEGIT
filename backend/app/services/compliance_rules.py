from typing import Optional
from app.models.schemas import ScanCreate


class ComplianceRule:
    """Represents a single compliance rule from Legal Metrology Rules 2011."""
    
    def __init__(self, rule_id: str, name: str, description: str, severity: str = "error"):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.severity = severity


COMPLIANCE_RULES = [
    ComplianceRule(
        rule_id="LM-001",
        name="Manufacturer/Packer/Importer Name and Address",
        description="Name and address of manufacturer/packer/importer must be clearly mentioned",
        severity="error"
    ),
    ComplianceRule(
        rule_id="LM-002",
        name="Net Quantity Declaration",
        description="Net quantity must be declared in standard units (g, kg, ml, L)",
        severity="error"
    ),
    ComplianceRule(
        rule_id="LM-003",
        name="MRP Declaration",
        description="Maximum Retail Price (MRP) must be clearly mentioned including tax",
        severity="error"
    ),
    ComplianceRule(
        rule_id="LM-004",
        name="Manufacture/Packing Date",
        description="Month and year of manufacture or packing must be mentioned",
        severity="error"
    ),
    ComplianceRule(
        rule_id="LM-005",
        name="Consumer Care Details",
        description="Consumer care name, address, and contact details must be provided",
        severity="warning"
    ),
    ComplianceRule(
        rule_id="LM-006",
        name="Country of Origin",
        description="Country of origin must be mentioned for imported goods",
        severity="error"
    ),
    ComplianceRule(
        rule_id="LM-007",
        name="Expiry/Best Before Date",
        description="Expiry date or best before date must be mentioned for perishable items",
        severity="error"
    ),
    ComplianceRule(
        rule_id="LM-008",
        name="MRP Inclusive of All Taxes",
        description="MRP should be inclusive of all taxes",
        severity="error"
    ),
    ComplianceRule(
        rule_id="LM-009",
        name="Unit Price Declaration",
        description="Unit price per kg or litre should be declared",
        severity="warning"
    ),
    ComplianceRule(
        rule_id="LM-010",
        name="Vegetarian/Non-Vegetarian Logo",
        description="Green/Red dot mark for vegetarian/non-vegetarian products",
        severity="info"
    ),
]


def get_all_rules():
    """Return all compliance rules."""
    return COMPLIANCE_RULES


def get_rule_by_id(rule_id: str) -> Optional[ComplianceRule]:
    """Get a specific rule by ID."""
    for rule in COMPLIANCE_RULES:
        if rule.rule_id == rule_id:
            return rule
    return None
