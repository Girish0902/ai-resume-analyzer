from typing import Dict


def analyze_fit(
    resume_dist: Dict[str, float],
    job_dist: Dict[str, float],
    job_category: str
) -> Dict:
    """
    Explainable Resume–Job Fit Reasoning Engine
    """

    # ---------- SAFETY CHECK ----------
    if not job_dist:
        return {
            "classification": "INSUFFICIENT DATA",
            "reasoning": (
                "The job description is too short or vague to extract meaningful skills. "
                "Please provide a more detailed job description for accurate fit analysis."
            )
        }

    if not resume_dist:
        return {
            "classification": "INSUFFICIENT DATA",
            "reasoning": (
                "The resume does not contain enough recognizable skills for comparison."
            )
        }

    # ---------- DOMINANT DOMAINS ----------
    dominant_job_domain = max(job_dist, key=job_dist.get)
    dominant_resume_domain = max(resume_dist, key=resume_dist.get)

    # ---------- FIT LOGIC ----------
    if dominant_job_domain == dominant_resume_domain:
        classification = "ALIGNED"
        reasoning = (
            f"Both the resume and job emphasize **{dominant_job_domain}**, "
            "indicating strong role alignment."
        )

    elif resume_dist.get(dominant_job_domain, 0) >= 0.3:
        classification = "PARTIALLY ALIGNED"
        reasoning = (
            f"The job focuses on **{dominant_job_domain}**, and the resume shows "
            "some relevant experience, but the primary focus differs."
        )

    else:
        classification = "MISALIGNED"
        reasoning = (
            f"The job requires strong **{dominant_job_domain}** expertise, "
            f"while the resume primarily emphasizes **{dominant_resume_domain}**."
        )

    return {
        "classification": classification,
        "reasoning": reasoning
    }
