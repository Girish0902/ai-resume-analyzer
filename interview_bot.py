class InterviewBot:
    """
    AI Interviewer that conducts a mock interview using Groq (OpenAI Client).
    """
    def __init__(self, client):
        self.client = client
        self.model = "llama3-70b-8192"

    def generate_question(self, job_description: str, history: list) -> str:
        """
        Generates the next interview question based on history.
        """
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
        
        prompt = f"""
        You are a professional Hiring Manager conducting a technical interview.
        
        JOB DESCRIPTION:
        {job_description}

        INTERVIEW HISTORY:
        {history_text}

        TASK:
        Generate the next interview question.
        - If this is the start, ask a "Tell me about yourself" or specific opener related to the job.
        - If the candidate answered, follow up or ask a new relevant technical/behavioral question.
        - Keep it professional and challenging.
        - ONLY output the question.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception:
            return "Could you tell me more about your experience with this role?"

    def evaluate_answer(self, question: str, answer: str) -> str:
        """
        Provides feedback on the candidate's answer.
        """
        prompt = f"""
        You are an Interview Coach.
        Evaluate the candidate's answer to the question: "{question}"
        Candidate's Answer: "{answer}"
        
        Provide concise, constructive feedback on:
        1. Clarity
        2. Relevance
        3. Quality of content
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception:
            return "Good answer, let's move on."
