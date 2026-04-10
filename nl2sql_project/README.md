# 🚀 NL2SQL System using FastAPI

## 📌 Overview
This project converts **natural language queries** into **SQL queries** and executes them on a SQLite database.  
It ensures accurate results by executing queries directly on the database, avoiding hallucinated outputs.

---

## 🎯 Features
- 🔹 Natural Language → SQL conversion using LLM
- 🔹 Executes queries on real SQLite database
- 🔹 Returns only actual database results
- 🔹 Handles invalid or unrelated queries gracefully
- 🔹 FastAPI backend with interactive Swagger UI

---

## 🛠️ Tech Stack
- **Python**
- **FastAPI**
- **SQLite**
- **Groq API (LLaMA 3.1 model)**

---

## ⚙️ Project Flow
# 🚀 NL2SQL System using FastAPI

## 📌 Overview
This project converts **natural language queries** into **SQL queries** and executes them on a SQLite database.  
It ensures accurate results by executing queries directly on the database, avoiding hallucinated outputs.

---

## 🎯 Features
- 🔹 Natural Language → SQL conversion using LLM
- 🔹 Executes queries on real SQLite database
- 🔹 Returns only actual database results
- 🔹 Handles invalid or unrelated queries gracefully
- 🔹 FastAPI backend with interactive Swagger UI

---

## 🛠️ Tech Stack
- **Python**
- **FastAPI**
- **SQLite**
- **Groq API (LLaMA 3.1 model)**

---

## ⚙️ Project Flow
User Question → LLM → SQL Query → SQLite Database → Result

---

## 📂 Project Structure
```plaintex
nl2sql_project/
│
├── api.py              # Main FastAPI application
├── clinic.db           # SQLite database
├── requirements.txt    # Dependencies
├── README.md           # Project documentation
├── .env.example        # Sample environment variables
├── .gitignore          # Ignored files
```

---

## ▶️ How to Run
```bash

### 1️⃣ Clone the Repository
git clone https://github.com/Devenzz/NL2SQl_Project
cd nl2sql_project

### 2️⃣ Install Dependencies
pip install -r requirements.txt

### 3️⃣ Setup Environment Variables
Create a .env file and add:

GROQ_API_KEY=  your_api_key_here

### 4️⃣ Run the Application
python -m uvicorn api:app --reload

### 5️⃣ Open Swagger UI
http://127.0.0.1:8000/docs

🧪 Example Queries

{
  "question": "How many patients do we have?"
}

{
  "question": "Show patients whose age is greater than 40"
}

```
## 👨‍💻 Author
**Devendra Gangurde**

🔗 [LinkedIn Profile](https://www.linkedin.com/in/devendra-gangurde-43620a262/)
