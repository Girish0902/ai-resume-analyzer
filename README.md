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

# AI-Based Resume Analyzer & Resume–Job Fit Reasoning System

## Problem Statement

Job seekers often struggle to understand how well their resume aligns with specific job requirements. Traditional Applicant Tracking Systems (ATS) provide scores but lack explainability, leaving candidates confused about why they match or mismatch. This system addresses the need for transparent, evidence-based resume-job fit analysis using AI-driven reasoning.

## System Overview

This is a modular, explainable AI system that parses resumes, analyzes job descriptions, and provides comprehensive compatibility insights. It uses heuristic methods for ATS scoring and skill distribution analysis for fit reasoning, integrated with a career guidance chatbot. The system is built with Python and Streamlit, designed for deployment on Hugging Face Spaces.

## Features

### 1. Resume Parsing
- Accepts PDF resumes
- Extracts clean text using PyPDF2
- Identifies skills through keyword matching with synonyms
- Handles missing sections gracefully

### 2. Job Description Analysis
- Parses job description text
- Extracts required and preferred skills
- Detects role category (Frontend/Backend/Data/Cloud/Security)

### 3. Skill Distribution Analysis
- Categorizes skills into domains: Frontend, Backend, Data, Cloud, Security, General
- Produces normalized distribution vectors (percentages)

### 4. ATS Compatibility Score
- Heuristic score (0–100) based on:
  - Skill match percentage
  - Keyword coverage
  - Resume length sanity
  - Section presence
- Clearly stated as an approximation, not a real ATS

### 5. Resume–Job Fit Reasoning
- Compares resume vs. job skill distributions
- Classifies fit as: ALIGNED, PARTIALLY ALIGNED, MISALIGNED
- Generates evidence-based reasoning without generic text

### 6. Career Guidance Chatbot
- Uses Gemini LLM integration (configurable to OpenAI/HF API)
- Answers questions strictly based on analysis results
- Uses exact system prompt to prevent hallucination
- Explains alignment, misalignments, and improvement directions

### 7. Streamlit UI
- Clean, professional interface
- PDF upload for resumes
- Text area for job descriptions
- Displays ATS score, fit classification, skill match summary
- Integrated chatbot for follow-up questions

## Limitations

- Relies on keyword matching; may miss context-dependent skills
- Heuristic ATS score is not equivalent to real ATS systems
- Skill extraction depends on predefined keyword lists
- Chatbot responses limited to provided analysis context
- No fine-tuning of models; uses prompt-based LLM integration
- PDF parsing may fail on complex or scanned documents

## Disclaimer

This tool is a decision-support system, not a real ATS. It provides heuristic approximations for educational and informational purposes only. Results should not be considered definitive hiring decisions. The system does not guarantee job placement or accuracy in all scenarios. Users should consult professional career advisors for personalized guidance.

## Installation & Usage

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up API key for LLM (e.g., GOOGLE_API_KEY for Gemini)
4. Run the app: `streamlit run app.py`
5. Upload a resume PDF and enter job description
6. Click "Analyze" to get results
7. Use the chatbot for follow-up questions

## Deployment on Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Upload all files to the repository
3. Set environment variables for API keys
4. The app will run automatically

## Dependencies

- streamlit
- PyPDF2
- google-generativeai (or openai, huggingface_hub for alternatives)

## Architecture

- `resume_parser.py`: Handles PDF parsing and skill extraction
- `job_parser.py`: Parses job descriptions and detects categories
- `skill_analyzer.py`: Analyzes skill distributions
- `ats_scoring.py`: Computes heuristic ATS scores
- `fit_reasoning.py`: Performs fit classification and reasoning
- `chatbot.py`: Manages LLM interactions
- `app.py`: Streamlit UI integration

Each module has a single responsibility, ensuring modularity and maintainability.
