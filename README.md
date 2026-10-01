# EduGenie - AI Learning Assistant

FastAPI + HTML/CSS/JavaScript + Google Gemini powered learning assistant.

## Features
- Ask a Question
- Explain a Topic
- Generate Quiz
- Summarize Notes
- Create a 7-day Learning Path

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` from `.env.example` and add your Gemini API key.

Run:

```powershell
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000`.

## Note about quota
If Gemini returns HTTP 429 / `RESOURCE_EXHAUSTED`, the app shows a friendly quota message instead of the raw server error. This does not bypass Gemini quota limits.
