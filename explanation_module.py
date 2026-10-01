from functools import lru_cache

from config import settings
from gemini_client import generate_text


@lru_cache(maxsize=1)
def _local_pipeline():
    from transformers import pipeline
    return pipeline(
        "text2text-generation",
        model=settings.local_explainer_model,
        device=-1,
    )


def _local_explain(topic: str, level: str) -> str:
    prompt = (
        f"Explain {topic} to a {level} student in simple language. "
        "Use a short definition, 3 key points, and one example."
    )
    result = _local_pipeline()(prompt, max_new_tokens=220, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_topic(topic: str, level: str = "beginner") -> str:
    if settings.use_local_explainer:
        try:
            return _local_explain(topic, level)
        except Exception:
            # If the optional local model is unavailable, Gemini remains a
            # reliable fallback rather than making the whole application fail.
            pass

    prompt = f"""You are EduGenie, a patient teacher.

Explain this topic to a {level} learner:
{topic}

Use this structure:
- Simple definition
- How it works / main idea
- 3 key points
- One easy example
- One quick memory tip

Avoid unnecessary jargon and keep it concise.
"""
    return generate_text(prompt, temperature=0.3, max_output_tokens=1600)
