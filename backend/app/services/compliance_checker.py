from typing import List, Dict, Any, Optional
import re
from app.services.compliance_rules import get_all_rules, ComplianceRule
from app.models.schemas import ScanCreate


class ComplianceChecker:
    """Check compliance of scanned product data against Legal Metrology Rules 2011."""

    def __init__(self):
        self.rules = get_all_rules()

    def check_compliance(self, scan_data: ScanCreate) -> Dict[str, Any]:
        """
        Check compliance of scan data against all rules.
        Returns a dict with compliance status and list of checks.
        """
        checks = []
        violations = []

        for rule in self.rules:
            check = self._check_rule(rule, scan_data)
            checks.append(check)
            if not check["is_compliant"]:
                violations.append(check)

        compliant_count = sum(1 for c in checks if c["is_compliant"])
        total = len(checks)

        if compliant_count == total:
            status = "compliant"
        elif compliant_count == 0:
            status = "non_compliant"
        else:
            status = "partial"

        return {
            "status": status,
            "checks": checks,
            "violations": violations,
            "summary": {
                "total_rules": total,
                "compliant": compliant_count,
                "non_compliant": len(violations),
                "compliance_percentage": (compliant_count / total * 100) if total > 0 else 0
            }
        }

    def _check_rule(self, rule: ComplianceRule, scan_data: ScanCreate) -> Dict[str, Any]:
        """Check a single rule against scan data."""
        raw = scan_data.raw_text or ""
        is_compliant = False
        details = ""

        if rule.rule_id == "LM-001":
            if scan_data.manufacturer or scan_data.packer or scan_data.importer:
                is_compliant = True
                details = "Manufacturer/Packer/Importer information found"
            else:
                details = "Missing manufacturer/packer/importer information"

        elif rule.rule_id == "LM-002":
            if scan_data.net_quantity:
                is_compliant = True
                details = f"Net quantity declared: {scan_data.net_quantity}"
            else:
                details = "Net quantity not declared"

        elif rule.rule_id == "LM-003":
            if scan_data.mrp:
                is_compliant = True
                details = f"MRP declared: {scan_data.mrp}"
            else:
                details = "MRP not declared"

        elif rule.rule_id == "LM-004":
            if scan_data.manufacture_date:
                is_compliant = True
                details = f"Manufacture date: {scan_data.manufacture_date}"
            else:
                details = "Manufacture/packing date not mentioned"

        elif rule.rule_id == "LM-005":
            if scan_data.consumer_care:
                is_compliant = True
                details = f"Consumer care: {scan_data.consumer_care}"
            else:
                details = "Consumer care details not provided"

        elif rule.rule_id == "LM-006":
            if scan_data.country_of_origin:
                is_compliant = True
                details = f"Country of origin: {scan_data.country_of_origin}"
            else:
                details = "Country of origin not mentioned"

        elif rule.rule_id == "LM-007":
            if scan_data.expiry_date:
                is_compliant = True
                details = f"Expiry date: {scan_data.expiry_date}"
            else:
                details = "Expiry/best before date not mentioned"

        elif rule.rule_id == "LM-008":
            # Check MRP inclusive of all taxes - look for keyword evidence in OCR text
            if raw:
                tax_keywords = re.search(
                    r"(?:inclusive|inclusiv|incl\.?)\s*(?:of\s*)?(?:all\s*)?(?:tax|gst|vat|taxes)",
                    raw, re.IGNORECASE
                )
                if tax_keywords:
                    is_compliant = True
                    details = "MRP appears to be inclusive of taxes"
                elif scan_data.mrp:
                    is_compliant = True
                    details = f"MRP declared: {scan_data.mrp} (tax inclusion assumed)"
                else:
                    details = "Cannot confirm MRP is inclusive of all taxes"
            elif scan_data.mrp:
                is_compliant = True
                details = f"MRP declared: {scan_data.mrp} (tax inclusion assumed)"
            else:
                details = "Cannot confirm MRP inclusive of all taxes - MRP not found"

        elif rule.rule_id == "LM-009":
            # Check unit price declaration
            if raw:
                unit_price = re.search(
                    r"(?:unit\s*price|price\s*per\s*(?:kg|g|ml|l|litre|gram|kilogram))"
                    r"\s*[:\-\*]?\s*(.+)",
                    raw, re.IGNORECASE
                )
                if unit_price:
                    is_compliant = True
                    details = f"Unit price declared: {unit_price.group(1).strip()}"
                else:
                    details = "Unit price per kg/litre not declared (warning)"
            else:
                details = "Unit price per kg/litre not declared (warning)"

        elif rule.rule_id == "LM-010":
            # Check vegetarian/non-vegetarian logo
            if raw:
                veg_match = re.search(
                    r"(?:veg|vegetarian|non[\s\-]?veg|non[\s\-]?vegetarian|edible\s*oil|fssai)",
                    raw, re.IGNORECASE
                )
                if veg_match:
                    is_compliant = True
                    details = "Vegetarian/Non-vegetarian marking context detected"
                else:
                    details = "Vegetarian/Non-vegetarian logo could not be confirmed from text"
            else:
                details = "Vegetarian/Non-vegetarian logo could not be confirmed from text"

        return {
            "rule_id": rule.rule_id,
            "rule_name": rule.name,
            "is_compliant": is_compliant,
            "details": details,
            "severity": rule.severity
        }


compliance_checker = ComplianceChecker()
