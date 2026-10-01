from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qa(monkeypatch):
    monkeypatch.setattr(main, "answer_question", lambda text: "Mock answer")
    response = client.post("/qa", json={"text": "What is 2+2?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Mock answer"


def test_explain(monkeypatch):
    monkeypatch.setattr(main, "explain_topic", lambda text, level: "Mock explanation")
    response = client.post(
        "/explain", json={"text": "Photosynthesis", "level": "beginner"}
    )
    assert response.status_code == 200
    assert response.json()["answer"] == "Mock explanation"


def test_quiz(monkeypatch):
    quiz = [{
        "question": "2 + 2 = ?",
        "options": ["3", "4", "5", "6"],
        "answer": "4",
        "explanation": "Basic addition."
    }]
    monkeypatch.setattr(main, "generate_quiz", lambda text, count: quiz)
    response = client.post("/quiz", json={"text": "Addition", "count": 1})
    assert response.status_code == 200
    assert response.json()["quiz"][0]["answer"] == "4"


def test_summary(monkeypatch):
    monkeypatch.setattr(main, "summarize_text", lambda text: "Mock summary")
    response = client.post("/summarize", json={"text": "Long text"})
    assert response.status_code == 200
    assert response.json()["summary"] == "Mock summary"


def test_learning_path(monkeypatch):
    monkeypatch.setattr(
        main, "get_learning_recommendations", lambda topic, level, hours: "Mock path"
    )
    response = client.post(
        "/learn/recommendations",
        json={"topic": "Python", "level": "beginner", "hours_per_week": 5},
    )
    assert response.status_code == 200
    assert response.json()["learning_path"] == "Mock path"
