from gemini_client import generate_text

def summarize_text(text: str) -> str:
    prompt = f"""You are EduGenie, an educational summarizer.

Summarize the following material for a student.
Requirements:
- Preserve the important facts and meaning.
- Remove repetition and filler.
- Use a clear heading and bullet points when helpful.
- Keep technical terms that are necessary.
- Do not add facts that are not supported by the input.

Material:
{text}
"""
    return generate_text(prompt, temperature=0.2, max_output_tokens=1800)
