from openai import OpenAI
import streamlit as st
import os

from resume_parser import parse_resume
from job_parser import parse_job_description
from skill_analyzer import analyze_skill_distribution
from ats_scoring import compute_ats_score
from fit_reasoning import analyze_fit
from chatbot import Chatbot

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("AI-Based Resume Analyzer & Resume–Job Fit Reasoning System")
st.caption(
    "Upload a resume PDF and enter a job description to evaluate ATS compatibility "
    "and role alignment using explainable logic."
)

# ================= SIDEBAR INPUTS =================
with st.sidebar:
    st.header("Inputs")
    resume_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
    job_desc = st.text_area("Job Description", height=200)
    
    # Check for secrets first
    if "GROK_API_KEY" in st.secrets and st.secrets["GROK_API_KEY"]:
        api_key = st.secrets["GROK_API_KEY"]
    else:
        # User must provide their own key
        api_key = st.text_input("Grok API Key", type="password")

    # Initialize OpenAI Client (for Grok)
    client = None
    if api_key:
        try:
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1" if "gsk_" in api_key else "https://api.x.ai/v1", 
            )
        except Exception as e:
            st.sidebar.error(f"Error initializing API: {e}")

    analyze_btn = st.button("Analyze", type="primary")

# ================= CHATBOT INIT =================
chatbot = None
if client:
    try:
        chatbot = Chatbot(client=client)
    except Exception as e:
        st.sidebar.error(f"Error initializing chatbot: {e}")
else:
    st.sidebar.warning("API Key required to enable Chatbot.")

# ================= INITIAL SESSION STATE =================
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

# ================= RUN ANALYSIS =================
if analyze_btn:

    if not resume_file or not job_desc.strip():
        st.error("Please upload a resume PDF and provide a job description.")
        st.stop()

    with st.spinner("Analyzing resume-job compatibility..."):

        # Reset chat history for new analysis
        st.session_state.chat_history = []

        resume_data = parse_resume(resume_file)
        job_data = parse_job_description(job_desc)

        resume_dist = analyze_skill_distribution(resume_data["skills"])
        job_dist = analyze_skill_distribution(job_data["skills"])

        # NEW: Compute AI-powered ATS Score
        if client:
            ats_result = compute_ats_score(client, resume_data, job_data)
        else:
             ats_result = {"overall_score": 0, "summary": "API Key needed for scoring."}

        fit_result = analyze_fit(
            resume_dist,
            job_dist,
            job_data["category"]
        )

        # ✅ STORE RESULTS
        st.session_state.resume_data = resume_data
        st.session_state.job_data = job_data
        st.session_state.ats_result = ats_result
        st.session_state.fit_result = fit_result
        st.session_state.analyzed = True

# ================= SHOW RESULTS (STATE-BASED) =================
if st.session_state.analyzed:

    resume_data = st.session_state.resume_data
    job_data = st.session_state.job_data
    ats_result = st.session_state.ats_result
    fit_result = st.session_state.fit_result

    # ================= TABS FOR V2 FEATURES =================
    tab1, tab2, tab3, tab4 = st.tabs(["Analysis", "Cover Letter", "Resume Refinement", "Mock Interview"])

    with tab1:
        col1, col2 = st.columns(2)
        # ... (Existing ATS and Fit Panels)
        with col1:
            st.subheader("AI Match Score")
            st.metric("Overall Match", f"{ats_result.get('overall_score', 0)}/100")
            st.caption(ats_result.get("summary", "Analysis complete."))
            with st.expander("Match Breakdown"):
                breakdown = ats_result.get("breakdown", {})
                st.write(f"Skill Match: {breakdown.get('skill_match', 0)}%")
                st.write(f"Experience Relevance: {breakdown.get('experience_relevance', 0)}%")
                st.write(f"Formatting & Structure: {breakdown.get('formatting', 0)}%")
            if ats_result.get("missing_skills"):
                st.error(f"Missing Critical Skills: {', '.join(ats_result['missing_skills'])}")

        with col2:
            st.subheader("Resume–Job Fit")
            if fit_result["classification"] == "ALIGNED":
                st.success(fit_result["classification"])
            elif fit_result["classification"] == "PARTIALLY ALIGNED":
                st.warning(fit_result["classification"])
            else:
                st.error(fit_result["classification"])
            st.write(f"**Reasoning:** {fit_result['reasoning']}")

        st.subheader("Skill Match Summary")
        for domain, job_skills in job_data["skills"].items():
            resume_skills = resume_data["skills"].get(domain, [])
            matched = set(resume_skills) & set(job_skills)
            st.write(f"**{domain}** → {len(matched)}/{len(job_skills)} matched")

    with tab2:
        st.header("AI Cover Letter Generator")
        from cover_letter_generator import generate_cover_letter
        
        tone = st.selectbox("Select Tone", ["Professional", "Enthusiastic", "Confident", "Humble"])
        if st.button("Generate Cover Letter"):
            if client:
                with st.spinner("Drafting your cover letter..."):
                    letter = generate_cover_letter(client, resume_data["text"], job_data["raw_text"], tone)
                    st.text_area("Generated Cover Letter", letter, height=400)
                    st.download_button("Download as Text", letter, file_name="Cover_Letter.txt")
            else:
                st.error("API Key required.")

    with tab3:
        st.header("Resume Refinement")
        from resume_refiner import refine_resume_section

        st.info("Select a text block from your resume (copy-paste below) to let AI rewrite it for this job.")
        
        user_text = st.text_area("Paste Resume Section (e.g., Experience Bullet Points)", height=150)
        
        if st.button("Refine Section"):
            if user_text and client:
                with st.spinner("Refining your resume..."):
                    refinement_result = refine_resume_section(client, user_text, job_data["raw_text"])
                    
                    if "error" in refinement_result:
                        st.error(refinement_result["error"])
                    else:
                        for item in refinement_result.get("improvements", []):
                            with st.expander(f"Original: {item['original'][:50]}...", expanded=True):
                                st.write(f"**Original:** {item['original']}")
                                st.success(f"**Rewrite:** {item['rewrite']}")
                                st.caption(f"**Reason:** {item['explanation']}")
            elif not client:
                st.error("API Key required.")
            else:
                st.warning("Please paste some text to refine.")

    with tab4:
        st.header("Mock Interview Simulator")
        from interview_bot import InterviewBot

        if "interview_history" not in st.session_state:
            st.session_state.interview_history = []
        if "interview_active" not in st.session_state:
            st.session_state.interview_active = False
            
        if st.button("Start/Reset Interview"):
            if client:
                st.session_state.interview_active = True
                st.session_state.interview_history = []
                interviewer = InterviewBot(client)
                first_q = interviewer.generate_question(job_data["raw_text"], [])
                st.session_state.interview_history.append({"role": "assistant", "content": first_q})
                st.rerun()
            else:
                st.error("API Key required.")

        if st.session_state.interview_active:
            if client:
                interviewer = InterviewBot(client)
                
                # Display history
                for msg in st.session_state.interview_history:
                    with st.chat_message(msg["role"]):
                        st.write(msg["content"])
                        if msg.get("feedback"):
                            st.info(f"Feedback: {msg['feedback']}")

                # User input
                if answer := st.chat_input("Your answer..."):
                    st.session_state.interview_history.append({"role": "user", "content": answer})
                    with st.chat_message("user"):
                        st.write(answer)
                    
                    # feedback
                    last_q = st.session_state.interview_history[-2]["content"]
                    feedback = interviewer.evaluate_answer(last_q, answer)
                    
                    # next question
                    with st.spinner("Interviewer is thinking..."):
                        next_q = interviewer.generate_question(job_data["raw_text"], st.session_state.interview_history)
                        st.session_state.interview_history[-1]["feedback"] = feedback # Attach feedback to user answer
                        st.session_state.interview_history.append({"role": "assistant", "content": next_q})
                        st.rerun()
            else:
                st.error("API Key required to continue interview.")


    # ================= CHATBOT =================
    if chatbot:
        st.subheader("Career Guidance Chatbot")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display chat history first
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Accept user input
        if prompt := st.chat_input("Ask about resume improvement or job fit..."):
            
            # Add user message to state and display it immediately
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Generate response
            with st.spinner("Thinking..."):
                response = chatbot.ask_question(
                    prompt,
                    context={
                        "resume_data": resume_data,
                        "job_data": job_data,
                        "ats_result": ats_result,
                        "fit_result": fit_result
                    }
                )

            # Add assistant response to state and display it immediately
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)
