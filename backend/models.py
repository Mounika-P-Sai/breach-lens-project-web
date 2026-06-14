"""
Pydantic models / schemas for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


# ── Auth ────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=200)
    password: str = Field(..., min_length=4, max_length=200)


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    token: str
    user: dict


class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    created_at: str


# ── Scan ────────────────────────────────────────────────

class ScanRequest(BaseModel):
    url: str = Field(..., max_length=2000)


class Vulnerability(BaseModel):
    type: str
    severity: str
    description: str
    recommendation: str
    risk_score: Optional[float] = None
    breach_probability: Optional[str] = None
    financial_loss: Optional[str] = None
    fix_cost: Optional[str] = None


class ScanStats(BaseModel):
    total_vulnerabilities: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    average_risk_score: float
    total_financial_loss: str
    total_fix_cost: str


class ScanResponse(BaseModel):
    id: str
    user_id: str
    url: str
    status: str
    results: List[Vulnerability]
    stats: ScanStats
    created_at: str


# ── Report ──────────────────────────────────────────────

class ReportResponse(BaseModel):
    id: str
    user_id: str
    scan_id: str
    file_path: str
    summary: dict
    created_at: str


# ── Security Posture ────────────────────────────────────

class SecurityPosture(BaseModel):
    score: float
    rating: str
    reason: str


class ComplianceAssessment(BaseModel):
    owasp: float
    gdpr: float
    iso27001: float


class BreachScenarioItem(BaseModel):
    vulnerability: str
    severity: str
    risk_score: float
    attack_path: List[str]
    business_impact: str
    estimated_financial_impact: str
    risk_level: str


class ExecutiveSummary(BaseModel):
    target_url: str
    total_vulnerabilities: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    overall_risk_score: float
    risk_level: str
    estimated_financial_exposure: str
    top_priority_risks: list
    priority_action: str


class ScanComparison(BaseModel):
    previous: dict
    current: dict
    delta: dict
    overall: str


# ── Dashboard / Stats ──────────────────────────────────

class DashboardStats(BaseModel):
    total_scans: int
    total_vulnerabilities: int
    average_risk_score: float
    total_financial_loss: str
    vulnerability_distribution: dict
    severity_breakdown: dict
    recent_scans: list
    risk_trend: list
    security_posture: Optional[SecurityPosture] = None
    compliance: Optional[ComplianceAssessment] = None


class ScanDetailResponse(BaseModel):
    scan: ScanResponse
    executive_summary: ExecutiveSummary
    security_posture: SecurityPosture
    compliance: ComplianceAssessment
    breach_scenarios: List[BreachScenarioItem]
