"""
prep_doc.py — Generates a pre-meeting prep document using Ollama.
"""

import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.2"

PREP_DOC_PROMPT = """You are preparing someone for a coffee chat. Generate a concise, 
useful pre-meeting document based on the information below.

Structure the document as:

## About [Name]
2-3 sentence summary of who they are and what they do.

## Their background
- Current role and key responsibilities
- Career arc (where they've been, what trajectory they're on)
- Education

## Interesting angles
2-3 specific, non-generic things worth asking about or mentioning
(based on actual details in their profile — not generic advice).

## Suggested talking points
3-4 specific questions tailored to this person. Make them good —
not "what do you do day to day" but substantive questions that show
you did your homework.

## Potential connections
Any overlaps between your background and theirs (shared companies,
industries, schools, skills, interests).

---
Person's profile data:
{profile_json}

Meeting context: {meeting_context}

Your background: {your_background}

Be specific and direct. Avoid generic filler."""


def generate_prep_doc(
    person_name: str,
    profile_data: dict,
    meeting_context: str = "General coffee chat / networking",
    your_background: str = "",
) -> dict:
    prompt = PREP_DOC_PROMPT.format(
        profile_json=json.dumps(profile_data, indent=2),
        meeting_context=meeting_context,
        your_background=your_background or "Not provided",
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return {
        "person_name": person_name,
        "document": response.choices[0].message.content,
        "format": "markdown",
    }