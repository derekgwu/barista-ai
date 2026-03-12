"""
resume.py — Extracts structured information from a resume PDF or DOCX.
Uses Ollama (local, free, no API key needed).
"""

import json
from pathlib import Path
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.2"

EXTRACTION_PROMPT = """Extract the following from this resume as JSON:
{
  "name": "",
  "email": "",
  "phone": "",
  "current_role": "",
  "summary": "",
  "experience": [
    {"title": "", "company": "", "start": "", "end": "", "description": ""}
  ],
  "education": [
    {"school": "", "degree": "", "field": "", "year": ""}
  ],
  "skills": [],
  "source": "resume"
}

Return ONLY valid JSON, no other text."""


def parse_resume(file_path: str) -> dict:
    path = Path(file_path)
    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _parse_pdf(path)
    elif suffix in (".docx", ".doc"):
        return _parse_docx(path)
    else:
        return {"error": f"Unsupported file type: {suffix}"}


def _parse_pdf(path: Path) -> dict:
    """Extract text from PDF then send to Ollama."""
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except ImportError:
        return {"error": "pdfplumber not installed. Run: pip install pdfplumber"}

    return _ask_llm(text)


def _parse_docx(path: Path) -> dict:
    """Extract text from DOCX then send to Ollama."""
    try:
        from docx import Document
        doc = Document(str(path))
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except ImportError:
        return {"error": "python-docx not installed. Run: pip install python-docx"}

    return _ask_llm(text)


def _ask_llm(resume_text: str) -> dict:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You extract structured data from resumes. Return only valid JSON."},
            {"role": "user", "content": f"Resume:\n\n{resume_text}\n\n{EXTRACTION_PROMPT}"},
        ],
        temperature=0,
    )
    return _safe_parse(response.choices[0].message.content)


def _safe_parse(text: str) -> dict:
    try:
        clean = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(clean)
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse JSON: {e}", "raw": text}