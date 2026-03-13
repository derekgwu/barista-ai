"""
Cappuccino AI — Strands agent that researches a company and job,
then generates a pre-networking-call prep document.

Install:
    pip install 'strands-agents[ollama]' duckduckgo-search

Run:
    python agent.py
"""

from strands import Agent, tool
from strands.models.ollama import OllamaModel
from ddgs import DDGS


# ── Tools ─────────────────────────────────────────────────────────────────────

@tool
def search_company_culture(company: str) -> str:
    """Search for a company's culture, values, and work environment."""
    with DDGS() as ddgs:
        results = list(ddgs.text(
            f"{company} company culture values work environment employee experience",
            max_results=4
        ))
    if not results:
        return f"No culture info found for {company}."
    return "\n\n".join(
        f"Source: {r['href']}\n{r['title']}\n{r['body']}" for r in results
    )


@tool
def search_job_description(company: str, job_title: str) -> str:
    """Search for what a specific job role involves at a company."""
    with DDGS() as ddgs:
        results = list(ddgs.text(
            f"{job_title} at {company} responsibilities day in the life what does it involve",
            max_results=4
        ))
    if not results:
        return f"No job info found for {job_title} at {company}."
    return "\n\n".join(
        f"Source: {r['href']}\n{r['title']}\n{r['body']}" for r in results
    )


@tool
def search_company_news(company: str) -> str:
    """Search for recent news and developments about the company."""
    with DDGS() as ddgs:
        results = list(ddgs.text(
            f"{company} news 2025 2026 recent announcements",
            max_results=4
        ))
    if not results:
        return f"No recent news found for {company}."
    return "\n\n".join(
        f"Source: {r['href']}\n{r['title']}\n{r['body']}" for r in results
    )


@tool
def search_interview_tips(company: str, job_title: str) -> str:
    """Search for interview and networking tips specific to this company and role."""
    with DDGS() as ddgs:
        results = list(ddgs.text(
            f"{company} {job_title} interview networking tips questions to ask",
            max_results=3
        ))
    if not results:
        return f"No interview tips found for {job_title} at {company}."
    return "\n\n".join(
        f"Source: {r['href']}\n{r['title']}\n{r['body']}" for r in results
    )


@tool
def generate_prep_document(
    company: str,
    job_title: str,
    culture_info: str,
    job_info: str,
    news_info: str,
    interview_tips: str,
    student_background: str = "",
) -> str:
    """
    Generate a pre-networking-call prep document from all researched information.
    Call this LAST after all research tools have been used.
    """
    # Use a separate Ollama call to generate the final doc
    from openai import OpenAI
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

    prompt = f"""You are helping a student prep for a networking coffee chat.
    
Company: {company}
Role they're interested in: {job_title}
Student background: {student_background or "Not provided"}

Research gathered:

COMPANY CULTURE:
{culture_info}

JOB ROLE INFO:
{job_info}

RECENT NEWS:
{news_info}

NETWORKING/INTERVIEW TIPS:
{interview_tips}

Generate a concise pre-networking-call prep document with these sections:

## About {company}
2-3 sentences on what the company does and their current focus.

## The {job_title} role at {company}
What this role actually involves day to day. Try to avoid describing
the role generically

## Company culture
Key things to know about working there.

## Recent news to mention
1-2 recent developments worth referencing in conversation.

## Smart questions to ask
4-5 specific, non-generic questions tailored to this role and company.
Avoid "what does your day look like" — ask things that show research.

## How to position yourself
{f"Based on the student's background: {student_background}" if student_background else "General tips for a student networking into this role."}

Keep it tight — this is a reference doc, not an essay."""

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


# ── Agent setup ───────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are Cappuccino AI, a networking prep assistant for students.

When given a company and job title, you MUST follow these steps in order:
1. Search for company culture
2. Search for what the job involves
3. Search for recent company news
4. Search for interview/networking tips
5. Generate the prep document using ALL the research you gathered

Do not skip any research steps. Do not generate the prep document until 
you have completed all four research searches. Be thorough."""

model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2",
)

agent = Agent(
    model=model,
    tools=[
        search_company_culture,
        search_job_description,
        search_company_news,
        search_interview_tips,
        generate_prep_document,
    ],
    system_prompt=SYSTEM_PROMPT,
)


# ── Run ───────────────────────────────────────────────────────────────────────

def prep_for_networking_call(company: str, job_title: str, student_background: str = ""):
    prompt = f"""Prep me for a networking coffee chat.
Company: {company}
Role I'm interested in: {job_title}
My background: {student_background or "Computer science student looking to break into tech"}

Research the company and role thoroughly, then generate my prep document."""

    print(f"\nResearching {job_title} at {company}...\n")
    print("=" * 60)

    response = agent(prompt)

    print("\n" + "=" * 60)
    return str(response)


if __name__ == "__main__":
    company = input("Company name: ").strip() or "Stripe"
    job_title = input("Job title: ").strip() or "Product Manager"
    background = input("Your background (press enter to skip): ").strip()

    result = prep_for_networking_call(company, job_title, background)
    print(result)