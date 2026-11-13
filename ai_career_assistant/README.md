# AI Career Assistant

A Streamlit application for resume analysis, skill-gap identification, interview preparation, and career planning using an LLM API.

## Features

- Upload a resume as PDF, DOCX, or TXT, or paste resume text.
- Analyze resume strengths, gaps, ATS readability, and evidence-based bullet improvements.
- Compare a candidate profile with a target role and optional job description.
- Generate role-specific interview questions, answer frameworks, and follow-up questions.
- Generate a practical four-week career action plan.
- Validate inputs and keep API credentials in environment variables.
- RAG is documented as a future extension; it is not represented as implemented.

## Requirements

- Python 3.10+
- An OpenAI API key with access to `gpt-4o-mini`

## Setup (Windows PowerShell)

```powershell
cd path\to\ai_career_assistant
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Add your API key to `.env`:

```env
OPENAI_API_KEY=your_real_api_key
```

Run:

```powershell
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## Project structure

```text
ai_career_assistant/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── src/
    ├── __init__.py
    ├── llm_service.py
    ├── prompts.py
    ├── resume_parser.py
    └── validation.py
```

## Security and privacy

- Never commit `.env` or paste your API key into source code.
- Do not upload sensitive personal documents unless you are comfortable processing them.
- When AI features are used, extracted resume text and prompts are sent to the configured LLM API.
- This starter app does not store resumes in a database. Streamlit session state holds generated results during the session.
- For production, add authentication, rate limits, request-size limits, logging controls, and a clear retention policy.

## RAG roadmap (future work)

RAG is planned, not implemented in this version. A sensible next phase:

1. Add an opt-in knowledge base containing trusted career resources and user-provided job descriptions.
2. Extract text from documents, split into chunks, and attach source metadata.
3. Create embeddings and store vectors in FAISS or ChromaDB.
4. Retrieve the most relevant chunks for a user query.
5. Pass retrieved context to the LLM and show source references.
6. Add tests for retrieval relevance, prompt injection in documents, and unsupported claims.

## Suggested tests

- Empty resume input should show a validation message.
- Unsupported file type should be rejected.
- PDF/DOCX/TXT extraction should return readable text.
- Missing API key should not crash the app.
- Invalid API key or API failure should show a clear error.
- Generated suggestions must not introduce unverified skills, metrics, or experience.

## Resume project description

**AI Career Assistant | Python, Streamlit, LLM API, Prompt Engineering**

- Developed a Streamlit-based career-support application for resume analysis, skill-gap identification, and role-specific interview preparation.
- Designed structured prompts to generate personalized career guidance, resume feedback, and interview questions with follow-up prompts.
- Implemented PDF/DOCX/TXT resume input, validation, and environment-based API-key management.
- Documented a future RAG extension for source-grounded retrieval from career resources and job descriptions.

Only claim features as completed after you have run and tested them yourself.
