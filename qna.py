from gemini_client import generate_text

SYSTEM = """You are EduGenie, a friendly educational assistant.
Answer the student's question accurately and concisely.
Use simple language, short paragraphs, and bullets when useful.
If the question is ambiguous, state the assumption you made.
Do not invent citations or claim to have browsed the web.
"""

def answer_question(question: str) -> str:
    prompt = f"""{SYSTEM}

Student question:
{question}

Give the direct answer first, then a short explanation and one useful example when appropriate.
"""
    return generate_text(prompt, temperature=0.3, max_output_tokens=1500)
