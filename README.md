🌟 Adaptive Learning Platform
Real-Time Personalized Learning using Apache Spark Streaming, Agentic AI & Explainable AI

A next-generation AI-powered learning system that continuously analyzes student performance, generates quizzes automatically, evaluates them using LLMs, and provides personalized learning recommendations — with clear explanations.

This project integrates three major AI disciplines (as required in your PDF):

🌊 Stream Processing → Apache Spark Streaming + Kafka

🤖 Agentic AI → Autonomous AI Tutor

🔍 Explainable AI → Human-readable reasoning


51bdad4d-1795-49fc-afc9-74b6864…

🚀 Project Overview

The Adaptive Learning Platform monitors students’ learning behavior (quiz scores, engagement, time spent) and uses real-time data + AI to create a fully personalized learning journey.

🔥 Key Capabilities

📄 AI-generated quizzes from uploaded PDFs

🧠 LLM-based quiz evaluation (Groq API – free developer tier)

🌊 Real-time analytics using Kafka + Spark Streaming

🤖 Agentic AI tutor that decides next best topic

🔍 Explainable AI engine that justifies recommendations

🖥 React dashboard for visualization & insights

🧭 System Workflow
flowchart LR
A[📄 Upload Material] --> B[🤖 AI Quiz Generator]
B --> C[📝 Student Takes Quiz]
C --> D[🧠 LLM Evaluates Answers]
D --> E[🌊 Kafka → Spark Streaming]
E --> F[📊 Processed Performance Summary]
F --> G[🤖 Agentic AI Tutor Recommends Next Topic]
G --> H[🔍 Explainable AI Generates Reason]
H --> I[📈 React Dashboard Updates Live]

⚙️ Features
📄 1. AI-Generated Quizzes

Upload PDFs or text → LLM (Groq) generates:

MCQs

Short-answer questions

Comprehensive topic coverage

🧠 2. AI-Based Quiz Evaluation

Objective answers → auto-graded

Subjective answers → Groq LLM grading

Explanation included (“scored 7/10 because…”)

🌊 3. Real-Time Stream Processing (Spark + Kafka)

Kafka collects:

Quiz submission events

Time spent

Topic engagement

Spark Streaming performs:

Aggregations

Weak-topic detection

Trend analysis


51bdad4d-1795-49fc-afc9-74b6864…

🤖 4. Agentic AI Tutor

Based on Spark outputs, the tutor:

Analyzes learner strengths & weaknesses

Recommends next topics or revision modules

Adapts to the student automatically


51bdad4d-1795-49fc-afc9-74b6864…

🔍 5. Explainable AI (XAI)

Every recommendation includes reasons like:

“Low quiz performance detected.”

“Time spent is significantly below expected.”


51bdad4d-1795-49fc-afc9-74b6864…

🖥 6. React Dashboard

Beautiful interface showing:

Quiz results

Real-time graphs

Personalized recommendations

Explanation panel

🏗 Architecture
React Frontend (Upload → Quiz → Dashboard)
                │
                ▼
         FastAPI Backend
  LLM Quiz Gen | Evaluation | PDF Extract
                │
                ▼
           Apache Kafka
                │
                ▼
      Apache Spark Streaming
 Process quiz_score | time_spent | difficulty trends
                │
                ▼
     Agentic AI Tutor + Explainable AI
                │
                ▼
        React Dashboard (Live Stats)

📂 Folder Structure
adaptive-learning-platform/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── models/
│   ├── requirements.txt
│   ├── venv/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│
├── stream_processing/
│   ├── spark_stream_processor.py
│   ├── kafka_topics.txt
│
└── README.md

🛠 Tech Stack
Frontend

React

TailwindCSS

Axios

Recharts

Backend

FastAPI

Python 3.10

Groq API

PyMuPDF (PDF extraction)

Pydantic

Streaming Layer

Apache Kafka

Apache Spark Streaming

AI Modules

Groq LLM (Quiz Generation + Evaluation)

Rule-based explanations / XAI

Agentic tutor logic

Database

MongoDB

📈 Student Experience
1️⃣ Upload Material

PDF → AI extracts text → quiz auto-generated.

2️⃣ Take Quiz

Dynamic MCQs + subjective answers.

3️⃣ AI Evaluates

Scores + explanation → stored → streamed to Kafka.

4️⃣ Spark Streaming

Analyzes:

Low score topics

High difficulty patterns

Learning progress

5️⃣ AI Tutor Decides

Recommends:

Revision topic

New topic

Practice quiz

6️⃣ Explanation Shown

Clear reason like:

“Recommended because your score on SVM was below 60%.”

🧪 How to Run
1. Backend (FastAPI)
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

2. Frontend (React)
cd frontend
npm install
npm start

3. Kafka
zookeeper-server-start
kafka-server-start

4. Spark Streaming
python stream_processing/spark_stream_processor.py

🚀 Future Enhancements

Chat-based AI tutor

Learning path graphs

Teacher admin view

Topic difficulty heatmaps

📘 Academic Requirements – Completed

Based on PDF:
✔ Implemented learner interaction streams using Kafka + Spark Streaming
✔ Autonomous agent personalizing content (Agentic AI)
✔ Explanations for every recommendation (Explainable AI)


51bdad4d-1795-49fc-afc9-74b6864…
