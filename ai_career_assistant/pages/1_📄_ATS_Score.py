import streamlit as st
import os
from src.llm_service import LLMService
from src.resume_parser import parse_resume
from src.prompts import SYSTEM_PROMPT, resume_analysis_prompt
from src.validation import validate_name, validate_resume_text

st.set_page_config(page_title="ATS Score", page_icon="📄")
st.title("📄 ATS Resume Analyzer")
st.caption("Upload your resume and paste the job description to get an ATS score and feedback.")

# We need the API key globally
api_key = os.getenv("GROQ_API_KEY")
llm = LLMService(provider="groq", api_key=api_key, model="openai/gpt-oss-120b")

# Two columns layout (like the 3rd image)
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded = st.file_uploader("PDF or DOCX", type=["pdf", "docx", "txt"], label_visibility="collapsed")
    if uploaded:
        st.success(f"✅ {uploaded.name} uploaded successfully.")

with col2:
    st.subheader("2. Job Description")
    job_desc = st.text_area("Paste the job requirements here...", height=200, label_visibility="collapsed")
    if job_desc:
        st.caption(f"{len(job_desc)} characters")

st.divider()

if st.button("⚡ Check ATS Score", type="primary", use_container_width=True):
    if not uploaded or not job_desc:
        st.error("Please upload a resume AND paste a job description.")
    else:
        with st.spinner("Analyzing resume against job description..."):
            resume_text = parse_resume(uploaded.name, uploaded.getvalue())
            
            # Run the AI
            prompt = f"""
            Here is a Job Description:
            {job_desc}
            
            Here is my Resume:
            {resume_text}
            
            Give me an ATS Match Score out of 100, and explain why. Then list 5 specific bullet points to add to my resume to beat the ATS.
            """
            result = llm.generate(prompt, SYSTEM_PROMPT)
            st.markdown("### 📊 Analysis Results")
            st.info(result)