"""Structured prompt templates for the LLM."""

SYSTEM_PROMPT = (
    "You are a senior career coach and technical recruiter with 10+ years of "
    "experience. Give concrete, honest, actionable feedback. Use clear headings "
    "and bullet points. Never invent skills the candidate does not have."
)


def resume_analysis_prompt(resume: str, role: str) -> str:
    return f"""Analyze this resume for the role: {role}.
Sections:
1. Overall Impression (3-4 sentences)
2. Strengths (bullet list with evidence)
3. Weaknesses (bullet list, be specific)
4. ATS Improvements (formatting, keywords, measurable results)
5. Top 5 Concrete Edits (rewrite suggestions)

Resume:
\"\"\"
{resume}
\"\"\""""


def skill_gap_prompt(resume: str, role: str) -> str:
    return f"""Compare this resume with skills required for {role}.
Output:
1. Skills already demonstrated (with evidence)
2. Missing / weak skills
3. Prioritized learning plan (skill -> why -> resource idea)
4. Match score /100 with a one-line justification

Resume:
\"\"\"
{resume}
\"\"\""""


def interview_prep_prompt(resume: str, role: str) -> str:
    return f"""Generate interview prep for a candidate applying to {role}.
Return:
1. 8 Technical Questions (easy -> hard), each with a 3-6 line model answer
2. 6 Behavioral / HR questions with STAR guidance
3. 2 follow-up / counter-questions the candidate can ask the interviewer
4. 3 red flags to avoid for this role

Resume:
\"\"\"
{resume}
\"\"\""""


def career_guidance_prompt(resume: str, role: str) -> str:
    return f"""Create a 6-month career roadmap to reach {role}.
Return:
1. Where they are today
2. 30-60-90 day plan
3. Skills to build (ordered by impact)
4. 3 portfolio project ideas
5. Networking & job-search strategy
6. Metrics to track progress

Resume:
\"\"\"
{resume}
\"\"\""""