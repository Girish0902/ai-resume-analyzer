import json

def compute_ats_score(client, resume_data: dict, job_data: dict) -> dict:
    """
    Computes an AI-powered ATS score using Groq (OpenAI Client).
    Returns a JSON object with score and reasoning.
    """
    
    resume_text = resume_data.get("text", "")
    job_text = job_data.get("raw_text", "")
    
    prompt = f"""
    You are an expert AI Resume Analyzer and Recruiter. 
    Evaluate the candidate's resume against the job description strictly and objectively.
    
    JOB DESCRIPTION:
    {job_text}
    
    RESUME:
    {resume_text}
    
    TASK:
    1. Analyze the relevance of the resume to the job.
    2. Provide an honest Match Score (0-100).
    3. List missing critical skills.
    4. Provide a brief professional summary of the fit.
    
    OUTPUT FORMAT (JSON ONLY):
    {{
        "overall_score": <number 0-100>,
        "breakdown": {{
            "skill_match": <number 0-100>,
            "experience_relevance": <number 0-100>,
            "formatting": <number 0-100>
        }},
        "missing_skills": ["skill1", "skill2"],
        "summary": "<short analysis>"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192", # Using robust model on Groq
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"AI Scoring Failed: {e}")
        # Fallback to a basic structure if AI fails, to prevent crash
        return {
            "overall_score": 0,
            "breakdown": {"skill_match": 0, "experience_relevance": 0, "formatting": 0},
            "missing_skills": ["Error in AI analysis"],
            "summary": f"Could not compute score due to error: {str(e)}"
        }
