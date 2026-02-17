import re
from typing import Dict, List
from PyPDF2 import PdfReader

# -------------------------------
# Skill Keywords Dictionary
# -------------------------------
SKILL_KEYWORDS = {
    "Frontend": [
        "html", "css", "javascript", "react", "angular", "vue",
        "bootstrap", "typescript", "responsive design", "ui/ux", "figma"
    ],
    "Backend": [
        "python", "java", "nodejs", "express", "django", "flask",
        "spring", "php", "c#", ".net", "api", "rest", "graphql",
        "microservices"
    ],
    "Data": [
        "sql", "mysql", "postgresql", "mongodb", "pandas", "numpy",
        "machine learning", "data analysis", "spark", "etl",
        "data warehouse", "power bi", "tableau"
    ],
    "Cloud": [
        "aws", "azure", "gcp", "docker", "kubernetes",
        "terraform", "ci/cd", "jenkins", "lambda", "s3"
    ],
    "Security": [
        "cybersecurity", "penetration testing", "vulnerability assessment",
        "siem", "ids", "ips", "incident response", "firewall", "encryption"
    ],
    "General": [
        "git", "linux", "agile", "scrum", "problem solving",
        "communication", "teamwork"
    ],
}

# -------------------------------
# PDF Text Extraction
# -------------------------------
def extract_text_from_pdf(pdf_file) -> str:
    """
    Safely extract text from PDF.
    Always returns a string (never None).
    """
    try:
        reader = PdfReader(pdf_file)
        text_chunks = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

        return " ".join(text_chunks).lower()

    except Exception as e:
        print(f"[Resume Parser] PDF extraction failed: {e}")
        return ""


# -------------------------------
# Skill Extraction
# -------------------------------
def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extract skills using keyword matching.
    Returns ONLY domains with matched skills.
    """
    skills_found: Dict[str, List[str]] = {}

    for domain, keywords in SKILL_KEYWORDS.items():
        matched = set()

        for kw in keywords:
            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, text, re.IGNORECASE):
                matched.add(kw)

        if matched:
            skills_found[domain] = sorted(matched)

    return skills_found


# -------------------------------
# MAIN PARSER
# -------------------------------
def parse_resume(pdf_file) -> Dict:
    """
    Parse resume PDF and return structured data
    REQUIRED schema for ATS:
    {
        "text": str,
        "skills": Dict[str, List[str]]
    }
    """
    text = extract_text_from_pdf(pdf_file)
    skills = extract_skills(text)

    return {
        "text": text,        # ✅ REQUIRED for ATS similarity
        "skills": skills     # ✅ Clean, deduplicated skills
    }
