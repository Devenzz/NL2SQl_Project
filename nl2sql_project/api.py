from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os
from dotenv import load_dotenv
from openai import OpenAI

# LOAD ENV
load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=groq_key,
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI()

# Request model
class QueryRequest(BaseModel):
    question: str

# Clean SQL
def clean_sql(query):
    return query.replace("```sql", "").replace("```", "").strip()

# Generate SQL
def generate_sql(question):
    prompt = f"""
Convert the question into SQL query ONLY if it is related to the database.

Database:
Table: patients(patient_id, name, age, gender)

Rules:
- Only return SQL
- If unrelated → return INVALID QUERY

Question: {question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return clean_sql(response.choices[0].message.content)

# Run SQL
def run_sql(query):
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    cursor.execute(query)
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    conn.close()
    return columns, result

# API Endpoint
@app.post("/query")
def query_db(request: QueryRequest):
    sql_query = generate_sql(request.question)

    if "INVALID QUERY" in sql_query.upper():
        return {
            "error": "Data not available"
        }

    try:
        columns, result = run_sql(sql_query)

        return {
            "sql": sql_query,
            "columns": columns,
            "result": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }