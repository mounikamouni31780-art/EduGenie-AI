import json
import re
from typing import Any

from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _normalize_quiz(data: Any, count: int) -> list[dict]:
    if isinstance(data, dict):
        data = data.get("questions") or data.get("quiz") or []

    if not isinstance(data, list):
        raise ValueError("Quiz response is not a list.")

    normalized = []
    for item in data[:count]:
        if not isinstance(item, dict):
            continue
        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", item.get("correct_answer", ""))).strip()
        explanation = str(item.get("explanation", "")).strip()

        if question and isinstance(options, list) and len(options) == 4 and answer:
            normalized.append({
                "question": question,
                "options": [str(x) for x in options],
                "answer": answer,
                "explanation": explanation,
            })

    if len(normalized) < min(count, 1):
        raise ValueError("Gemini returned an invalid quiz structure.")
    return normalized


def generate_quiz(text: str, count: int = 3) -> list[dict]:
    schema = """{
      "questions": [
        {
          "question": "string",
          "options": ["string", "string", "string", "string"],
          "answer": "exactly one option string",
          "explanation": "short explanation"
        }
      ]
    }"""

    prompt = f"""You are EduGenie, an educational quiz generator.

Create exactly {count} multiple-choice questions from the supplied material.
Rules:
- Every question must be answerable from the material.
- Exactly 4 options per question.
- Exactly one correct answer.
- The answer field must exactly match one option.
- Include a short explanation.
- Return ONLY valid JSON. No Markdown fences.

JSON shape:
{schema}

Material:
{text}
"""
    raw = generate_text(prompt, temperature=0.3, max_output_tokens=3000)
    cleaned = clean_json_block(raw)

    try:
        parsed = json.loads(cleaned)
        return _normalize_quiz(parsed, count)
    except (json.JSONDecodeError, ValueError):
        # One repair pass makes the endpoint more robust against occasional
        # formatting mistakes while still requiring valid JSON at the end.
        repair = f"""Convert the following into valid JSON matching this exact schema:
{schema}
Return ONLY JSON.

Input:
{raw}
"""
        repaired = clean_json_block(
            generate_text(repair, temperature=0.0, max_output_tokens=3000)
        )
        parsed = json.loads(repaired)
        return _normalize_quiz(parsed, count)
