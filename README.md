---
title: AI Resume Analyzer
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.25.0
app_file: app.py
pinned: false
python_version: "3.10"
---

# 📄 AI-Based Resume Analyzer & Resume–Job Fit Reasoning System

An AI-powered resume analysis tool that evaluates how well a resume matches a job description. It uses **Groq's LLaMA 3.3 70B** model for intelligent ATS scoring, skill gap detection, cover letter generation, resume refinement, and mock interview simulation — all in a clean Streamlit interface.

> 🚀 **Live Demo:** [Hugging Face Space](https://huggingface.co/spaces/Girish0902/AI-RESUME-ANALYZER)  
> 💻 **GitHub:** [Girish0902/ai-resume-analyzer](https://github.com/Girish0902/ai-resume-analyzer)

---

## ✨ Features

### 1. 📊 AI Match Score (ATS Scoring)
- Powered by **LLaMA 3.3 70B via Groq API**
- Returns an honest match score (0–100)
- Breakdown across: **Skill Match**, **Experience Relevance**, **Formatting & Structure**
- Lists **missing critical skills**
- Provides a professional summary of resume-job fit

### 2. 🎯 Resume–Job Fit Reasoning
- Compares skill distributions between resume and job description
- Classifies fit as: `ALIGNED` / `PARTIALLY ALIGNED` / `MISALIGNED`
- Generates evidence-based reasoning (no generic text)
- Detects dominant skill domains: Frontend, Backend, Data, Cloud, Security

### 3. 🔍 Skill Match Summary
- Side-by-side domain-wise skill comparison
- Shows how many job-required skills are present in the resume
- Covers 6 domains: **Frontend, Backend, Data, Cloud, Security, General**

### 4. ✉️ AI Cover Letter Generator
- Generates personalized cover letters using AI
- Supports 4 tones: **Professional, Enthusiastic, Confident, Humble**
- Tailored to the specific job description and resume content
- Downloadable as a `.txt` file

### 5. ✏️ Resume Refinement
- Paste any resume section (experience bullets, summary, etc.)
- AI rewrites it using the **STAR method** (Situation, Task, Action, Result)
- Uses strong action verbs and quantified achievements
- Shows original vs. rewrite with explanation for each improvement

### 6. 🎤 Mock Interview Simulator
- AI acts as a professional hiring manager
- Generates contextual interview questions based on the job description
- Evaluates your answers on clarity, relevance, and content quality
- Provides constructive feedback after each answer
- Full conversation history displayed in a chat interface

### 7. 🤖 Career Guidance Chatbot
- Context-aware chatbot using Groq AI
- Answers questions strictly based on your resume analysis results
- Prevents hallucination by grounding responses in actual data
- Available after running analysis

---

## 🏗️ Architecture

```
ai-resume-analyzer/
├── app.py                    # Main Streamlit UI & tab routing
├── resume_parser.py          # PDF text extraction + skill keyword matching
├── job_parser.py             # Job description parsing + role category detection
├── skill_analyzer.py         # Normalized skill distribution vectors
├── ats_scoring.py            # AI-powered ATS score via Groq (JSON output)
├── fit_reasoning.py          # Explainable fit classification (ALIGNED/MISALIGNED)
├── chatbot.py                # Career guidance chatbot via Groq
├── cover_letter_generator.py # AI cover letter generation
├── resume_refiner.py         # STAR-method resume section rewriter
├── interview_bot.py          # Mock interview question generator + answer evaluator
├── requirements.txt          # Python dependencies
└── README.md
```

Each module has a **single responsibility**, ensuring modularity and maintainability.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend / UI** | Streamlit |
| **AI Model** | LLaMA 3.3 70B (`llama-3.3-70b-versatile`) |
| **AI Provider** | [Groq](https://console.groq.com) (OpenAI-compatible API) |
| **PDF Parsing** | PyPDF2 |
| **Skill Analysis** | Keyword matching + normalized distributions |
| **Language** | Python 3.10+ |
| **Deployment** | Hugging Face Spaces |

---

## ⚙️ Installation & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/Girish0902/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your Groq API key

Get a free API key at [console.groq.com](https://console.groq.com/keys).

**Option A — Streamlit secrets (recommended, persistent):**

Create the file `~/.streamlit/secrets.toml` (or `.streamlit/secrets.toml` inside the project):
```toml
GROK_API_KEY = "gsk_your_key_here"
```

**Option B — Enter in the UI:**  
Just paste your key into the sidebar text field each time you run the app.

### 4. Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🚀 Deployment on Hugging Face Spaces

1. Fork or push this repo to your HF Space (SDK: `streamlit`)
2. Go to your Space → **Settings** → **Variables and secrets**
3. Add a new secret: `GROK_API_KEY` = `gsk_your_key_here`
4. The app builds and runs automatically

> The `secrets.toml` file is gitignored and never pushed — your API key is always safe.

---

## 📦 Dependencies

```
PyPDF2          # PDF text extraction
scikit-learn    # ML utilities
numpy           # Numerical operations
openai          # OpenAI-compatible client (used with Groq)
groq            # Groq SDK
pillow          # Image handling
```

> `streamlit` is managed by Hugging Face Spaces directly (not in requirements.txt to avoid version conflicts).

---

## ⚠️ Limitations

- Skill extraction relies on **predefined keyword lists** — may miss context-dependent or niche skills
- PDF parsing may fail on **scanned or image-based** PDFs
- ATS score is an **AI approximation**, not a real ATS system score
- Chatbot responses are grounded in analysis context only, not general career advice
- No user authentication or resume storage

---

## 📋 Disclaimer

This tool is a **decision-support system**, not a real ATS. It provides AI-powered approximations for educational and informational purposes only. Results should not be considered definitive hiring decisions. Users should consult professional career advisors for personalized guidance.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) for blazing-fast LLaMA inference
- [Streamlit](https://streamlit.io) for the UI framework
- [Hugging Face](https://huggingface.co) for free Space hosting
