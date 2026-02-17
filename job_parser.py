import re
from typing import Dict, List


# -------------------------------
# Skill taxonomy (ATS-oriented)
# -------------------------------
SKILL_MAP: Dict[str, List[str]] = {
    "Frontend": [
        "html", "css", "javascript", "react", "angular", "vue",
        "typescript", "ui", "ux"
    ],
    "Backend": [
        "python", "java", "node", "express", "django", "flask",
        "spring", "api", "microservices"
    ],
    "Data": [
        "sql", "nosql", "data analysis", "data engineering",
        "pandas", "numpy", "spark", "airflow", "etl",
        "data warehouse", "big data"
    ],
    "Cloud": [
        "aws", "azure", "gcp", "docker", "kubernetes",
        "terraform", "ci/cd"
    ],
    "Security": [
        "cybersecurity", "security", "penetration testing",
        "siem", "soc", "nmap", "burp", "owasp",
        "incident response", "threat detection", "malware"
    ]
}


# -------------------------------
# Critical skills (used for penalties / reasoning)
# -------------------------------
CRITICAL_SKILLS: Dict[str, List[str]] = {
    "Data": ["spark", "airflow", "etl", "data warehouse"],
    "Security": ["siem", "incident", "threat", "malware"],
    "Backend": ["api", "microservices", "database"],
    "Cloud": ["aws", "docker", "kubernetes"],
}


# -------------------------------
# Helper: normalize text
# -------------------------------
def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


# -------------------------------
# MAIN: Job Description Parser
# -------------------------------
def parse_job_description(text: str) -> dict:
    """
    Extracts:
    - skills grouped by domain
    - dominant job category
    - raw JD text (for ATS semantic scoring)
    """

    raw_text = text.strip()
    text_norm = _normalize(raw_text)

    extracted_skills: Dict[str, List[str]] = {}

    # -------- Skill extraction --------
    for domain, skills in SKILL_MAP.items():
        matched = [
            skill for skill in skills
            if re.search(rf"\b{re.escape(skill)}\b", text_norm)
        ]
        if matched:
            extracted_skills[domain] = sorted(set(matched))

    # -------- Category inference (weighted) --------
    domain_scores = {
        domain: len(skills)
        for domain, skills in extracted_skills.items()
    }

    if domain_scores:
        category = max(domain_scores, key=domain_scores.get)
    else:
        category = "General"

    return {
        "raw_text": raw_text,          # REQUIRED for ATS scoring
        "skills": extracted_skills,    # Domain-wise skills
        "category": category           # Dominant role
    }
