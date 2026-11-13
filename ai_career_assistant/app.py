"""AI Career Assistant — Streamlit entry point (multi-provider)."""

import os
import streamlit as st
from dotenv import load_dotenv

from src.llm_service import LLMService, PROVIDERS, get_provider_config
from src.resume_parser import parse_resume
from src.prompts import (
    SYSTEM_PROMPT,
    resume_analysis_prompt,
    skill_gap_prompt,
    interview_prep_prompt,
    career_guidance_prompt,
)
from src.validation import validate_name, validate_resume_text

load_dotenv()

st.set_page_config(page_title="AI Career Assistant", page_icon="🎯", layout="wide")
st.title("🎯 AI Career Assistant")
st.caption("Python • Streamlit • Groq / OpenAI / Gemini • Prompt Engineering")

# ---------- Sidebar: provider + key + model ----------
with st.sidebar:
    st.header("⚙️ AI Provider")

    provider = st.selectbox(
        "Provider",
        options=list(PROVIDERS.keys()),
        index=0,  # Groq first = free default
        help="Groq is free with no credit card. OpenAI needs paid credits.",
    )
    cfg = get_provider_config(provider)

    env_key = os.getenv(cfg["env_key"], "").strip()
    if env_key:
        st.success(f"Key loaded from .env (`{cfg['env_key']}`)")
        api_key = env_key
    else:
        api_key = st.text_input(
            f"{cfg['env_key']} (paste here)",
            type="password",
        ).strip()

    model = st.selectbox("Model", cfg["models"], index=0)

    st.divider()
    st.markdown("**Roadmap**")
    st.caption("Phase 4: RAG with FAISS/Chroma — next lesson.")

# ---------- Inputs ----------
st.subheader("1. Your details")
c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Your name")
with c2:
    role = st.selectbox(
        "Target role",
        ["Data Analyst", "Data Scientist", "Python Developer", "AI Engineer",
         "Machine Learning Engineer"],
    )

st.subheader("2. Upload your resume")
uploaded = st.file_uploader("PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])

resume_text = ""
if uploaded:
    try:
        resume_text = parse_resume(uploaded.name, uploaded.getvalue())
        ok, msg = validate_resume_text(resume_text)
        (st.success if ok else st.warning)(
            f"Parsed {len(resume_text.split())} words from {uploaded.name}."
            if ok else msg
        )
    except Exception as e:
        st.error(f"Could not parse resume: {e}")

if resume_text:
    with st.expander("Preview extracted text"):
        st.text(resume_text[:3000] + ("..." if len(resume_text) > 3000 else ""))

# ---------- Run ----------
st.subheader("3. Run analysis")
name_ok, _ = validate_name(name)
ready = name_ok and bool(resume_text)

if st.button("🚀 Analyze my career", type="primary", disabled=not ready):

    if not api_key:
        st.error(f"Missing API key. Add `{cfg['env_key']}` to .env or paste it in the sidebar.")
        st.stop()

    try:
        llm = LLMService(provider=provider, api_key=api_key, model=model)
    except Exception as e:
        st.error(str(e))
        st.stop()

    def run(prompt: str, label: str) -> str:
        try:
            with st.spinner(f"{label}..."):
                return llm.generate(prompt, SYSTEM_PROMPT)
        except Exception as e:
            msg = str(e)
            if "429" in msg or "rate_limit" in msg.lower():
                return (
                    "⏳ **Rate limit hit.** Wait ~30 seconds and try again, "
                    "or switch to a faster model in the sidebar "
                    "(`llama-3.1-8b-instant`)."
                )
            if "401" in msg or "invalid_api_key" in msg.lower():
                return f"🔑 **Invalid API key** for {provider}. Check the key and try again."
            return f"⚠️ {msg}"

    st.success(f"Welcome {name}! Analyzing for {role} using **{provider} / {model}**.")

    t1, t2, t3, t4 = st.tabs(
        ["📄 Resume Review", "🧩 Skill Gap", "🎤 Interview Prep", "🗺️ Career Roadmap"]
    )
    with t1:
        st.markdown(run(resume_analysis_prompt(resume_text, role), "Reviewing resume"))
    with t2:
        st.markdown(run(skill_gap_prompt(resume_text, role), "Comparing skills"))
    with t3:
        st.markdown(run(interview_prep_prompt(resume_text, role), "Generating questions"))
    with t4:
        st.markdown(run(career_guidance_prompt(resume_text, role), "Building roadmap"))