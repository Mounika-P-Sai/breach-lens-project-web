"""
Database Layer — MongoDB Atlas Backend
Replaces the old mock/file-based storage with live MongoDB collections.
All public methods keep the same signatures as before for backward compatibility.
"""

import uuid
from datetime import datetime
from typing import Optional
from services.mongodb_service import get_db


class MockDB:
    """
    Database interface backed by MongoDB Atlas.
    Connects via the `services.mongodb_service` module.
    """

    # ── Helpers ────────────────────────────────────────────

    @staticmethod
    def _format_user(user: Optional[dict]) -> Optional[dict]:
        """Convert MongoDB user doc -> old format (id instead of _id)."""
        if not user:
            return None
        user["id"] = str(user.pop("_id"))
        return user

    @staticmethod
    def _format_scan(scan: Optional[dict]) -> Optional[dict]:
        """Convert MongoDB scan doc -> old format."""
        if not scan:
            return None
        scan["id"] = str(scan.pop("_id"))
        return scan

    @staticmethod
    def _format_report(report: Optional[dict]) -> Optional[dict]:
        """Convert MongoDB report doc -> old format."""
        if not report:
            return None
        report["id"] = str(report.pop("_id"))
        return report

    # ── Users ──────────────────────────────────────────────

    @staticmethod
    def create_user(name: str, email: str, hashed_password: str) -> dict:
        db = get_db()
        user = {
            "_id": str(uuid.uuid4()),
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": "user",
            "created_at": datetime.utcnow().isoformat(),
        }
        db.users.insert_one(user)
        return MockDB._format_user(user)

    @staticmethod
    def get_user_by_email(email: str) -> Optional[dict]:
        db = get_db()
        user = db.users.find_one({"email": email})
        return MockDB._format_user(user)

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[dict]:
        db = get_db()
        user = db.users.find_one({"_id": user_id})
        return MockDB._format_user(user)

    # ── Scans ──────────────────────────────────────────────

    @staticmethod
    def create_scan(user_id: str, url: str, results: list, stats: dict) -> dict:
        db = get_db()
        scan_id = str(uuid.uuid4())
        scan = {
            "_id": scan_id,
            "user_id": user_id,
            "url": url,
            "status": "completed",
            "results": results,
            "stats": stats,
            "created_at": datetime.utcnow().isoformat(),
        }
        db.scans.insert_one(scan)

        # Also store each vulnerability individually in the vulnerabilities collection
        for r in results:
            vuln = {
                "_id": str(uuid.uuid4()),
                "scan_id": scan_id,
                "user_id": user_id,
                "vulnerability_type": r.get("type", "Unknown"),
                "severity": r.get("severity", "Medium"),
                "risk_score": r.get("risk_score", 0),
                "breach_probability": r.get("breach_probability", "N/A"),
                "financial_loss": r.get("financial_loss", "₹0"),
                "remediation_cost": r.get("fix_cost", "₹0"),
                "description": r.get("description", ""),
                "recommendation": r.get("recommendation", ""),
            }
            db.vulnerabilities.insert_one(vuln)

        return MockDB._format_scan(scan)

    @staticmethod
    def get_scans_by_user(user_id: str) -> list:
        db = get_db()
        scans = list(db.scans.find({"user_id": user_id}))
        return [MockDB._format_scan(s) for s in scans]

    @staticmethod
    def get_scan_by_id(scan_id: str) -> Optional[dict]:
        db = get_db()
        scan = db.scans.find_one({"_id": scan_id})
        return MockDB._format_scan(scan)

    @staticmethod
    def get_all_scans() -> list:
        db = get_db()
        scans = list(db.scans.find())
        return [MockDB._format_scan(s) for s in scans]

    # ── Reports ────────────────────────────────────────────

    @staticmethod
    def create_report(user_id: str, scan_id: str, file_path: str, summary: dict) -> dict:
        db = get_db()
        report = {
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "scan_id": scan_id,
            "file_path": file_path,
            "report_url": file_path,
            "summary": summary,
            "created_at": datetime.utcnow().isoformat(),
        }
        db.reports.insert_one(report)
        return MockDB._format_report(report)

    @staticmethod
    def get_reports_by_user(user_id: str) -> list:
        db = get_db()
        reports = list(db.reports.find({"user_id": user_id}))
        return [MockDB._format_report(r) for r in reports]

    @staticmethod
    def get_report_by_id(report_id: str) -> Optional[dict]:
        db = get_db()
        report = db.reports.find_one({"_id": report_id})
        return MockDB._format_report(report)
