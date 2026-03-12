"""
resume.py — Extracts structured information from a resume PDF or DOCX.
Uses Claude's vision/document capability for high accuracy.
"""

import json
import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

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
    """Read PDF as bytes and send inline — no file upload needed."""
    with open(path, "rb") as f:
        pdf_bytes = f.read()
 
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=[
            {
                "inline_data": {
                    "mime_type": "application/pdf",
                    "data": pdf_bytes,
                }
            },
            EXTRACTION_PROMPT,
        ],
    )
    return _safe_parse(response.text)
 
 
def _parse_docx(path: Path) -> dict:
    """Extract DOCX text with python-docx, then send to Gemini."""
    try:
        from docx import Document
        doc = Document(str(path))
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except ImportError:
        return {"error": "python-docx not installed. Run: pip install python-docx"}
 
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=f"Resume text:\n\n{text}\n\n{EXTRACTION_PROMPT}",
    )
    return _safe_parse(response.text)
 
 
def _safe_parse(text: str) -> dict:
    try:
        clean = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(clean)
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse JSON: {e}", "raw": text}