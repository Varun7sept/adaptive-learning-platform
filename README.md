📘 Adaptive Learning Platform – Stream Processing + Agentic AI + Explainable AI
A Real-Time Intelligent Tutoring System Powered by AI and Streaming Technologies

This project implements an Adaptive Learning Platform that personalizes learning paths for students using:

Stream Processing (Apache Kafka + Apache Flink)

Agentic AI (Autonomous Tutoring Agents)

Explainable AI (XAI) (Human-understandable explanations)

LLM-based Quiz Generation & Evaluation (Groq API)

It combines three subjects exactly as mentioned in the uploaded PDF:

Stream Processing

Agentic AI

Explainable AI


51bdad4d-1795-49fc-afc9-74b6864…

🚀 Project Overview

This system continuously monitors student learning behavior in real-time (quiz scores, study material engagement, performance trends) and dynamically adapts the content delivered to them.

✔ Key Features

AI-generated quizzes from uploaded study materials (PDF/text)

LLM-based answer evaluation using free Groq API

Real-time learner interaction streaming using Kafka

Live performance processing using Flink

Autonomous agent (Agentic AI) recommends next best topic

Explainable AI module provides clear reasons for recommendations

React-based dashboard for students to view progress & recommendations

🧭 High-Level Workflow
Student → Upload Material → AI generates Quiz
Student → Takes Quiz → AI Evaluates Answers
↓
Kafka Streams → Flink Aggregates Performance
↓
Agentic AI Tutor → Decides Next Topic
Explainable AI → Adds Reason
↓
React Dashboard → Shows Personalized Recommendations

🧠 Core Components
1. Stream Processing Layer – Kafka + Flink

Implements real-time learner interaction streams.
Flink performs:

Windowed aggregations

Performance trend detection

Topic-level difficulty estimation


51bdad4d-1795-49fc-afc9-74b6864…

Output is published to Kafka topic learner_summary.

2. Agentic AI Layer – Autonomous Tutor Agent

The AI tutor:

Reads processed summaries

Understands learner weaknesses

Decides the next topic / quiz / revision material

Adapts learning paths automatically


51bdad4d-1795-49fc-afc9-74b6864…

Example decisions:

"Recommend Review: Linear Regression"

"Unlock Next Topic: Logistic Regression"

3. Explainable AI Layer

Generates human-readable justification for each recommendation.

Examples:

“Topic recommended due to low quiz performance.”

“Less time spent compared to average.”


51bdad4d-1795-49fc-afc9-74b6864…

This ensures transparency and trust.

4. AI Quiz Generation & Evaluation

Uses Groq LLM API (free developer tier) to:

✅ Generate quizzes from uploaded PDFs
✅ Evaluate student answers (MCQ/short answers)
✅ Provide reasoning for marks

5. Frontend – React Dashboard

Students can:

Upload study material

Take quizzes

View live performance analytics

View recommended topics with explanations

🏗 Project Architecture
┌──────────────────────────────────────────┐
│               React Frontend             │
│ Upload → Quiz → Dashboard → Insights     │
└───────────────────────┬──────────────────┘
                        │ REST API
┌───────────────────────▼──────────────────┐
│                FastAPI Backend           │
│ Quiz Gen | PDF Extract | LLM Eval        │
└──────────────┬───────────┬──────────────┘
               │           │
        Kafka Producer     │
               │        MongoDB
┌──────────────▼───────────────────────────┐
│              Apache Kafka (Events)        │
└──────────────┬───────────────────────────┘
               │
┌──────────────▼───────────────────────────┐
│             Apache Flink Processor        │
│  Trend detection | Aggregation            │
└──────────────┬───────────────────────────┘
               │
┌──────────────▼───────────────────────────┐
│  Agentic AI Tutor + Explainable AI        │
└──────────────┬───────────────────────────┘
               │
        React Dashboard (Live Fetch)

📂 Folder Structure
adaptive-learning-platform/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   ├── utils/
│   ├── venv/
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│
├── stream_processing/
│   ├── flink_job.py
│   ├── kafka_setup.txt
│
└── README.md

⚙️ Tech Stack
Frontend

React.js

Axios (API calls)

Tailwind CSS

Recharts (performance graphs)

Backend

FastAPI

Python 3.10

Groq LLM API

PyMuPDF (PDF extraction)

Pydantic

Kafka-Python

Streaming

Apache Kafka

Apache Flink

Database

MongoDB Atlas

AI Modules

Groq LLM (quiz gen + evaluation)

Rule-based explanations

(Optional) SHAP for model explanations

🧪 How Students Experience the System

1. Upload Material
Student uploads a PDF chapter or notes.

2. Quiz Auto-Generated
LLM prepares 5–10 MCQ/short-answer questions.

3. Student Takes Quiz
Answers are evaluated instantly (LLM reasoning).

4. Stream Processing Activated
Kafka → Flink analyzes scores, time spent, patterns.

5. AI Tutor Recommends
System adapts learning path automatically.

6. Dashboard Shows
📊 Progress graphs
🎯 Next topic
💬 Explanation for each recommendation

🎯 Key Outcomes (As Required By PDF)
✔ Stream Processing Outcome

Implement learner interaction streams using Kafka + Flink.


51bdad4d-1795-49fc-afc9-74b6864…

✔ Agentic AI Outcome

Tutoring agent personalizes learning based on engagement & outcomes.


51bdad4d-1795-49fc-afc9-74b6864…

✔ Explainable AI Outcome

Generates transparent explanations for recommendations.


51bdad4d-1795-49fc-afc9-74b6864…

🚀 How to Run the Project (Local Setup)
1️⃣ Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

2️⃣ Frontend
cd frontend
npm install
npm start

3️⃣ Kafka
zookeeper-server-start
kafka-server-start

4️⃣ Flink
start-cluster
python flink_job.py

📌 Future Enhancements

Conversational AI Tutor

Learning path visualization

Multi-student analytics

Teacher admin panel

✔ How to Add This README to Your GitHub

Run this inside your project root folder:

cd adaptive-learning-platform

notepad README.md


Paste the above content → Save.

Then run:

git add README.md
git commit -m "Added project README"
git push
