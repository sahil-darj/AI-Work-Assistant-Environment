---
title: AI Work Assistant
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# 🤖 AI Work Assistant: OpenEnv Hub

### 🚀 What is this?
This is a **smart testing simulator** for AI agents. Instead of just "chatting" with an AI, this project gives the AI **real work tasks** to solve and gives it a score based on how well it did.

It was built specifically for the **Meta OpenEnv Hackathon**.

---

### 💼 What can the AI do?
The AI is tested on 3 real-world tasks:
1. **Email Triage (Easy)**: The AI reads emails and decides if they are Spam, Work, or Important.
2. **Code Review (Medium)**: The AI looks at buggy Python code and finds the error.
3. **Data Cleaning (Hard)**: The AI fixes a messy dataset by removing errors and duplicates.

---

### 🛠️ How to Run (3 Simple Steps)

1. **Install everything**:
```bash
pip install -r requirements.txt
```

2. **Add your API Key**:
Open the `.env` file and paste your OpenAI key.

3. **Start the Dashboard**:
```bash
python app.py
```
*Then open **http://localhost:8000** in your browser!*

---

### 🌟 Why this project is "Cool"?
* **Glassmorphic UI**: A beautiful, modern web dashboard to watch the AI work.
* **Neural Thoughts**: You can see exactly what the AI is "thinking" before it acts.
* **Reward Charts**: It automatically creates a graph of the AI's performance.
* **Pro Presentation**: Includes a built-in slide deck (`presentation.html`) for the demo.

---

### 📐 Technical Details (For Judges)
* **Framework**: OpenEnv Standard
* **Models**: Pydantic for data, FastAPI for web, Chart.js for graphs.
* **Interface**: implements `step()`, `reset()`, and `state()`.
* **Logging**: Follows strict `[START]`, `[STEP]`, and `[END]` requirements.

---

### 🐳 Docker Support
Build and run anywhere with one command:
`docker build -t openenv-hub .`
