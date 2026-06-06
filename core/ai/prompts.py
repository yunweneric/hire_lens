"""Prompt templates for Gemini API calls."""

ANALYZE_APPLICATION_PROMPT = """
You are an expert technical recruiter. Compare the candidate resume against the job description.

Return ONLY valid JSON with this exact structure:
{{
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1"],
  "skill_match_pct": 75.0,
  "ai_confidence": 0.85,
  "ats_score": 78.0,
  "ai_summary": "2-3 sentence summary of fit for this role",
  "suggestions": ["actionable tip 1", "actionable tip 2"],
  "recommendation": "Strong fit|Good fit|Moderate fit|Weak fit"
}}

Scoring guide for ats_score (0-100): overall suitability for the role.
recommendation must be one of: Strong fit, Good fit, Moderate fit, Weak fit.

Resume:
{resume_text}

Job Description (Markdown):
{job_description}
"""

EXTRACT_SKILLS_PROMPT = """
Extract technical skills, soft skills, frameworks, programming languages,
certifications, and tools from this resume.

Return JSON:
{{
  "technical_skills": [],
  "soft_skills": [],
  "certifications": [],
  "tools": []
}}

Resume:
{resume_text}
"""

ANALYZE_MATCH_PROMPT = """
Compare this resume against the job description.

Return JSON:
{{
  "matched_skills": [],
  "missing_skills": [],
  "skill_match_pct": 0.0,
  "ai_confidence": 0.0
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""

GENERATE_SUGGESTIONS_PROMPT = """
You are an ATS resume coach. Given the analysis context below,
return 5-8 specific, actionable improvements as JSON:
{{"suggestions": ["...", "..."]}}

Context:
{context}
"""
