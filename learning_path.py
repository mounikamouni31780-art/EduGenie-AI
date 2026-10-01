from gemini_client import generate_text


def generate_learning_path(topic: str, level: str = "beginner", days: int = 7) -> str:
    prompt = f"""You are EduGenie, a learning-path designer.

Create a practical {days}-day learning path for:
Topic: {topic}
Current level: {level}

Include:
- Goal
- Prerequisites
- Daily step-by-step topics
- Practice tasks
- A small project or revision activity
- Suggested resource TYPES such as books, documentation, courses, or videos

Make it realistic, progressive, and easy for a student to follow.
"""
    return generate_text(prompt, temperature=0.5, max_output_tokens=2600)
