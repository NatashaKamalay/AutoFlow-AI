import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"


def run_extraction(transcript: str) -> dict:
    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=0
    )

    prompt = f"""
You are an enterprise workflow extraction agent.

Given the following meeting transcript, extract:
1. a short summary
2. key decisions
3. action items with owner, deadline, and notes if available
4. blockers

Return ONLY valid JSON in this exact format:
{{
  "summary": "...",
  "decisions": ["..."],
  "tasks": [
    {{
      "task": "...",
      "owner": "...",
      "deadline": "...",
      "priority": "...",
      "status": "pending",
      "notes": "..."
    }}
  ],
  "blockers": ["..."]
}}

Rules:
- If any field is unknown, use null.
- Do not include markdown.
- Do not include explanation text.
- Output only JSON.

Transcript:
{transcript}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    text = response.content.strip()

    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()
    return json.loads(text)