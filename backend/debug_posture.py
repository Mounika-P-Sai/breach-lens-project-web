"""Quick posture debug script."""
from services.risk_engine import calculate_security_posture

vulns3 = [
    {"type": "SQL Injection", "severity": "Critical", "risk_score": 96},
    {"type": "Auth Weakness", "severity": "Critical", "risk_score": 88},
    {"type": "XSS", "severity": "High", "risk_score": 64.5},
    {"type": "CSRF", "severity": "High", "risk_score": 51},
    {"type": "IDOR", "severity": "High", "risk_score": 66.8},
    {"type": "Directory Listing", "severity": "Medium", "risk_score": 27},
    {"type": "Missing Headers", "severity": "Medium", "risk_score": 27},
    {"type": "Info Disclosure", "severity": "Low", "risk_score": 5},
]
r = calculate_security_posture(vulns3)
print(f"score={r['score']} rating={r['rating']} reason={r['reason']}")

# What if risk_score is missing?
vulns4 = [
    {"type": "SQL Injection", "severity": "Critical"},
    {"type": "Auth Weakness", "severity": "Critical"},
]
r4 = calculate_security_posture(vulns4)
print(f"No risk_score: score={r4['score']} rating={r4['rating']}")
