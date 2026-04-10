# NL2SQL System using FastAPI

## 🚀 Project Overview
This project converts natural language queries into SQL and executes them on a SQLite database.

## 🛠 Tech Stack
- Python
- FastAPI
- SQLite
- Groq LLM (LLaMA 3.1)

## 🔥 Features
- Natural Language → SQL conversion
- Executes queries on real database
- Prevents hallucination (uses only DB results)
- Handles invalid queries
- FastAPI backend with Swagger UI

## ▶️ How to Run

### 1. Clone Repository
```bash
git clone <your_repo_link>
cd nl2sql_project

## How it Works

1. User enters question in plain English
2. LLM (Groq) converts it into SQL query
3. SQL query runs on SQLite database
4. Results are returned to user