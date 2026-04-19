class Chatbot:
    """
    AI-powered career guidance chatbot using Groq (OpenAI Client).
    """

    def __init__(self, client):
        self.client = client
        self.model = "llama-3.3-70b-versatile"

    def ask_question(self, question: str, context: dict) -> str:
        
        # Unpacking context for clarity in the prompt
        resume_text = context["resume_data"].get("text", "No resume text available.")
        job_text = context["job_data"].get("raw_text", "No job description available.")
        ats_score = context["ats_result"]["overall_score"]
        fit_reasoning = context["fit_result"]["reasoning"]
        
        prompt = f"""
        You are an expert career coach and resume analyst helping a candidate improve their chances for a specific job.
        
        CONTEXT:
        - Job Description: {job_text}
        - Resume Content: {resume_text}
        - Computed ATS Score: {ats_score}/100
        - System Fit Analysis: {fit_reasoning}
        
        USER QUESTION: "{question}"
        
        INSTRUCTIONS:
        - Answer the user's question directly and concisely.
        - Use the provided context to give specific, evidence-based advice.
        - If the user asks about the score or fit, explain it using the context.
        - Do not hallucinate skills or experience not present in the resume.
        - Keep the tone professional, encouraging, and actionable.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I encountered an error: {str(e)}"
