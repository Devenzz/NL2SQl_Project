# app.py

import streamlit as st
import pandas as pd
import sqlite3
from groq import Groq

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Hospital NL2SQL Assistant",
    page_icon="🏥",
    layout="wide"
)

# =========================
# Custom CSS
# =========================
st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
        color: white;
    }

    .title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        color: #00FFAA;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #BBBBBB;
        margin-bottom: 30px;
    }

    .stButton>button {
        width: 100%;
        background-color: #00AAFF;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        height: 50px;
        border: none;
    }

    .sql-box {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
        overflow-x: auto;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Title
# =========================
st.markdown(
    '<div class="title">🏥 Hospital Database AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Ask questions in plain English and the AI will automatically
    generate SQL queries and fetch data from the hospital database.
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# API Key & Model
# =========================
api_key = "YOUR_API_KEY"

model_name = "llama-3.3-70b-versatile"

# =========================
# =========================
# Sidebar
# =========================
st.sidebar.title("🏥 Hospital NL2SQL")

st.sidebar.markdown(
    """
    ### 💡 Try Asking

    🔹 Total doctors  
    🔹 Show all patients  
    🔹 Unpaid bills  
    🔹 Highest experience doctor  
    🔹 All appointments  
    """
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    ### ⚡ Features

    ✅ AI SQL Generator  
    ✅ Instant Results  
    ✅ Smart Error Handling  
    ✅ Multi-Table Support  
    ✅ CSV Download  
    """
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    ### 🧠 Tech Stack

    `Python` • `Streamlit` • `SQLite`  
    `Groq LLM` 
    """
)

# =========================
# User Question
# =========================
user_question = st.text_area(
    "💬 Ask Your Question",
    placeholder="Example: Show all doctors with more than 10 years experience"
)

# =========================
# Function: Get Database Schema
# =========================
def get_schema(connection):

    schema = ""

    cursor = connection.cursor()

    tables = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()

    for table in tables:

        table_name = table[0]

        columns = cursor.execute(
            f"PRAGMA table_info({table_name})"
        ).fetchall()

        schema += f"\nTable: {table_name}\n"

        for column in columns:

            schema += f"- {column[1]} ({column[2]})\n"

    return schema

# =========================
# Function: Generate SQL
# =========================
def generate_sql(question, schema, client, model_name):

    prompt = f"""
You are an expert SQL generator.

Available Database Tables and Columns:
{schema}

Convert the following natural language question into SQL.

Rules:
1. Return only SQL query.
2. Do not explain anything.
3. Use valid SQLite syntax.
4. Use ONLY tables and columns from provided schema.
5. Carefully analyze the schema before generating SQL.
6. Generate the most relevant SQL query possible.

Examples:

Question: How many doctors are there?
SQL:
SELECT COUNT(*) AS total_doctors FROM doctors;

Question: Show all patients
SQL:
SELECT * FROM patients;

Question: Show unpaid bills
SQL:
SELECT * FROM billing
WHERE payment_status = 'Pending';

Question: Which doctor has highest experience?
SQL:
SELECT * FROM doctors
ORDER BY experience DESC
LIMIT 1;

Question: Show all appointments
SQL:
SELECT * FROM appointments;

Question:
{question}
"""

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    sql_query = response.choices[0].message.content

    sql_query = sql_query.replace("```sql", "")
    sql_query = sql_query.replace("```", "")
    sql_query = sql_query.strip()

    return sql_query

# =========================
# Main Button
# =========================
if st.button("🚀 Generate SQL & Execute"):

    if user_question.strip() == "":

        st.error("Please enter your question")

    else:

        try:

            # =========================
            # Connect Database
            # =========================
            conn = sqlite3.connect("clinic.db")

            # =========================
            # Get Schema
            # =========================
            schema = get_schema(conn)

            # =========================
            # Show Schema
            # =========================
            with st.expander("📂 Database Schema"):
                st.text(schema)

            # =========================
            # Create GROQ Client
            # =========================
            client = Groq(api_key=api_key)

            # =========================
            # Generate SQL
            # =========================
            with st.spinner("Generating SQL Query..."):

                sql_query = generate_sql(
                    user_question,
                    schema,
                    client,
                    model_name
                )

            # =========================
            # Display SQL Query
            # =========================
            st.subheader("📝 Generated SQL Query")

            st.markdown(
                f"""
                <div class="sql-box">
                <code>{sql_query}</code>
                </div>
                """,
                unsafe_allow_html=True
            )

            # =========================
            # Execute SQL Query
            # =========================
            try:

                result_df = pd.read_sql_query(
                    sql_query,
                    conn
                )

                # =========================
                # No Records Found
                # =========================
                if result_df.empty:

                    st.info(
                        "No records found for this query."
                    )

                else:

                    # =========================
                    # Show Result
                    # =========================
                    st.subheader("📊 Query Result")

                    st.dataframe(
                        result_df,
                        use_container_width=True
                    )

                    # =========================
                    # Download CSV
                    # =========================
                    csv = result_df.to_csv(
                        index=False
                    ).encode("utf-8")

                    st.download_button(
                        label="⬇️ Download Result CSV",
                        data=csv,
                        file_name="query_result.csv",
                        mime="text/csv"
                    )

            # =========================
            # Handle SQL Errors
            # =========================
            except Exception as query_error:

                error_message = str(query_error)

                if "no such column" in error_message:

                    st.warning(
                        "The requested column does not exist in the database."
                    )

                elif "no such table" in error_message:

                    st.warning(
                        "The requested table does not exist in the database."
                    )

                elif "syntax error" in error_message:

                    st.warning(
                        "Generated SQL query has syntax issue. Please try again."
                    )

                else:

                    st.warning(
                        "Unable to process this query. Try asking a different question."
                    )

            conn.close()

        except Exception as e:

            st.error(f"Error: {e}")

# =========================
# Footer
# =========================
st.markdown("---")

# st.markdown(
#     """
#     <center>
#     Built with ❤️ using Streamlit, Groq LLM, SQLite & Python
#     </center>
#     """,
#     unsafe_allow_html=True
# )