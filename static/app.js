async function readResponse(response) {
    const text = await response.text();

    try {
        return JSON.parse(text);
    } catch {
        if (response.status === 429 || text.includes("RESOURCE_EXHAUSTED")) {
            throw new Error(
                "Gemini API quota exceeded. Please wait for the quota to reset and try again."
            );
        }

        if (response.status === 500) {
            throw new Error(
                "Gemini service is temporarily unavailable. Please try again later."
            );
        }

        throw new Error(
            response.ok
                ? "The server returned an unexpected response."
                : `Server error (${response.status}). Please try again later.`
        );
    }
}

async function askQuestion() {
    const question = document.getElementById("question").value.trim();
    const result = document.getElementById("qaResult");
    if (!question) { result.textContent = "Please enter a question."; return; }
    result.textContent = "⏳ Thinking...";
    try {
        const response = await fetch("/qa", {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });
        const data = await readResponse(response);
        if (!response.ok) throw new Error(data.detail || "Something went wrong.");
        result.textContent = data.answer;
    } catch (error) { result.textContent = "❌ Error: " + error.message; }
}

async function explainTopic() {
    const topic = document.getElementById("explainTopic").value.trim();
    const level = document.getElementById("explainLevel").value;
    const result = document.getElementById("explainResult");
    if (!topic) { result.textContent = "Please enter a topic."; return; }
    result.textContent = "⏳ Preparing explanation...";
    try {
        const response = await fetch("/explain", {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic, level })
        });
        const data = await readResponse(response);
        if (!response.ok) throw new Error(data.detail || "Something went wrong.");
        result.textContent = data.explanation;
    } catch (error) { result.textContent = "❌ Error: " + error.message; }
}

async function generateQuiz() {
    const topic = document.getElementById("quizTopic").value.trim();
    const level = document.getElementById("quizLevel").value;
    const numberOfQuestions = Number(document.getElementById("questionCount").value);
    const result = document.getElementById("quizResult");
    if (!topic) { result.textContent = "Please enter a quiz topic."; return; }
    result.textContent = "⏳ Generating quiz...";
    try {
        const response = await fetch("/quiz", {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic, num_questions: numberOfQuestions, level })
        });
        const data = await readResponse(response);
        if (!response.ok) throw new Error(data.detail || "Something went wrong.");
        const quiz = data.quiz;
        let html = `<h3>📝 ${quiz.topic || "EduGenie"} Quiz</h3>`;
        const questions = quiz.questions || quiz;
        questions.forEach((q, index) => {
            html += `<div class="quiz-question"><h4>Question ${index + 1}</h4><p>${q.question}</p><div class="quiz-options">${q.options.map(option => `<div>🔘 ${option}</div>`).join("")}</div><p><strong>✅ Answer:</strong> ${q.answer}</p><p><strong>💡 Explanation:</strong> ${q.explanation}</p></div>`;
        });
        result.innerHTML = html;
    } catch (error) { result.textContent = "❌ Error: " + error.message; }
}

async function summarizeText() {
    const text = document.getElementById("summaryText").value.trim();
    const result = document.getElementById("summaryResult");
    if (!text) { result.textContent = "Please paste some study material."; return; }
    result.textContent = "⏳ Summarizing...";
    try {
        const response = await fetch("/summarize", {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });
        const data = await readResponse(response);
        if (!response.ok) throw new Error(data.detail || "Something went wrong.");
        result.textContent = data.summary;
    } catch (error) { result.textContent = "❌ Error: " + error.message; }
}

async function generateLearningPath() {
    const topic = document.getElementById("learningTopic").value.trim();
    const level = document.getElementById("learningLevel").value;
    const result = document.getElementById("learningResult");
    if (!topic) { result.textContent = "Please enter a topic."; return; }
    result.textContent = "⏳ Creating learning path...";
    try {
        const response = await fetch("/learn/recommendations", {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic, level, days: 7 })
        });
        const data = await readResponse(response);
        if (!response.ok) throw new Error(data.detail || "Something went wrong.");
        result.textContent = data.plan;
    } catch (error) { result.textContent = "❌ Error: " + error.message; }
}
