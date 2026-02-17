import json

def refine_resume_section(client, section_text: str, job_description: str) -> dict:
    """
    Rewrites a resume section to better match the job description.
    Returns JSON with original and rewritten bullet points.
    """
    prompt = f"""
    You are an expert resume writer. 
    Rewrite the following resume section (e.g., Experience or Summary) to align with the Job Description.
    Use the STAR method (Situation, Task, Action, Result) where possible.
    Quantify achievements.
    Use strong action verbs.

    JOB DESCRIPTION:
    {job_description}

    RESUME SECTION:
    {section_text}

    OUTPUT FORMAT (JSON ONLY):
    {{
        "improvements": [
            {{
                "original": "Managed a team",
                "rewrite": "Led a cross-functional team of 5 engineers to deliver project X...",
                "explanation": "Added specifics and action verbs."
            }}
        ]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}
