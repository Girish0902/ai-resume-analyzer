def generate_cover_letter(client, resume_text: str, job_text: str, tone: str = "Professional") -> str:
    """
    Generates a personalized cover letter using Groq (OpenAI Client).
    """
    prompt = f"""
    You are an expert career coach and professional writer.
    Write a compelling, personalized cover letter for the candidate based on their resume and the job description.

    JOB DESCRIPTION:
    {job_text}

    RESUME CONTENT:
    {resume_text}

    INSTRUCTIONS:
    1. Tone: {tone}.
    2. Address the hiring manager if possibly known, otherwise use "Hiring Manager".
    3. Highlight specific achievements from the resume that match the job requirements.
    4. Keep it concise (3-4 paragraphs).
    5. Do not include placeholders like [Your Name] unless absolutely necessary; try to infer from resume or use generic placeholders.
    6. Output ONLY the body of the letter (and closing), no pre-text.
    """

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating cover letter: {str(e)}"
