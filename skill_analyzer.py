from typing import Dict, List

def analyze_skill_distribution(skills: Dict[str, List[str]]) -> Dict[str, float]:
    """
    Convert skill lists into normalized distribution percentages.
    """
    total_skills = sum(len(v) for v in skills.values())
    if total_skills == 0:
        return {k: 0.0 for k in skills}

    distribution = {}
    for domain, skill_list in skills.items():
        distribution[domain] = round((len(skill_list) / total_skills) * 100, 1)

    return distribution
