from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from config import APP_NAME
from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import generate_learning_path

app = FastAPI(
    title=APP_NAME,
    description="Gemini-powered AI Learning Assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class QARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)


class ExplanationRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)
    level: str = "beginner"


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)
    num_questions: int = Field(default=5, ge=1, le=10)
    level: str = "beginner"


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=15000)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)
    level: str = "beginner"
    days: int = Field(default=7, ge=1, le=30)


def handle_gemini_error(error: Exception):
    message = str(error)
    if "429" in message or "RESOURCE_EXHAUSTED" in message or "quota" in message.lower():
        raise HTTPException(
            status_code=429,
            detail="Gemini API quota exceeded. Please wait for the quota to reset and try again.",
        )
    raise HTTPException(
        status_code=500,
        detail="Gemini service is temporarily unavailable. Please try again later.",
    )


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": APP_NAME},
    )


@app.get("/health")
async def health():
    return {"status": "ok", "app": APP_NAME}


@app.post("/qa")
async def qa(request: QARequest):
    try:
        answer = answer_question(request.question)
        return {"success": True, "question": request.question, "answer": answer}
    except Exception as e:
        handle_gemini_error(e)


@app.post("/explain")
async def explain(request: ExplanationRequest):
    try:
        explanation = explain_topic(request.topic, request.level)
        return {
            "success": True,
            "topic": request.topic,
            "level": request.level,
            "explanation": explanation,
        }
    except Exception as e:
        handle_gemini_error(e)


@app.post("/quiz")
async def quiz(request: QuizRequest):
    try:
        quiz_data = generate_quiz(request.topic, request.num_questions, request.level)
        return {"success": True, "quiz": {"topic": request.topic, "questions": quiz_data}}
    except Exception as e:
        handle_gemini_error(e)


@app.post("/summarize")
async def summarize(request: SummaryRequest):
    try:
        summary = summarize_text(request.text)
        return {"success": True, "summary": summary}
    except Exception as e:
        handle_gemini_error(e)


@app.post("/learn/recommendations")
async def learning_path(request: LearningPathRequest):
    try:
        plan = generate_learning_path(request.topic, request.level, request.days)
        return {"success": True, "plan": plan}
    except Exception as e:
        handle_gemini_error(e)
