import sqlite3
import google.generativeai as genai
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
import traceback

# Load environment variables from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize FastAPI and Jinja2 templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Define request model for JSON API
class QueryRequest(BaseModel):
    question: str

# Function to ask Gemini and extract clean SQL
def ask_gemini(prompt):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    text = response.text.strip()

    # Remove markdown/code block formatting
    if "```sql" in text:
        text = text.split("```sql")[1]
    elif "```" in text:
        text = text.split("```")[1]
    text = text.replace("```", "").strip()

    # Extract only SQL lines
    sql_lines = []
    for line in text.splitlines():
        if any(word in line.lower() for word in ["select", "from", "where", "group by", "order by", "limit", "sum", "avg", "as"]):
            sql_lines.append(line)

    clean_sql = "\n".join(sql_lines).strip()
    print("Cleaned SQL:", clean_sql)
    return clean_sql

# Function to run SQL on the database
def query_sql(sql):
    conn = sqlite3.connect("ecom.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result

# JSON API endpoint
@app.post("/ask")
def ask_question(data: QueryRequest):
    question = data.question
    print("Received question:", question)

    schema = """
    Tables:
    - eligibility(item_id, eligibility_datetime_utc, eligibility, message)
    - ad_sales(item_id, date, ad_sales, impressions, ad_spend, clicks, units_sold)
    - total_sales(item_id, date, total_sales, total_units_ordered)
    """

    prompt = f"""
You are an expert SQL assistant. Convert the following natural language question to a single clean SQL query using the schema below.

IMPORTANT: Respond ONLY with the SQL query. Do NOT include explanations or markdown formatting.

Schema:
{schema}

Question:
{question}
"""

    try:
        sql_query = ask_gemini(prompt)
        print("Generated SQL:", sql_query)
        result = query_sql(sql_query)
        print("Query result:", result)

        return {
            "question": question,
            "sql_generated": sql_query,
            "answer": result
        }
    except Exception as e:
        print("Error occurred:", e)
        traceback.print_exc()
        return {
            "error": str(e),
            "sql_generated": "Check Gemini output above"
        }

# Web UI route using HTML form
@app.get("/", response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
async def home(request: Request):
    answer = None
    sql_query = None

    if request.method == "POST":
        form = await request.form()
        question = form.get("question")

        schema = """
        Tables:
        - eligibility(item_id, eligibility_datetime_utc, eligibility, message)
        - ad_sales(item_id, date, ad_sales, impressions, ad_spend, clicks, units_sold)
        - total_sales(item_id, date, total_sales, total_units_ordered)
        """

        prompt = f"""
You are an expert SQL assistant. Convert the following natural language question to a single clean SQL query using the schema below.

IMPORTANT: Respond ONLY with the SQL query. Do NOT include explanations or markdown formatting.

Schema:
{schema}

Question:
{question}
"""

        try:
            sql_query = ask_gemini(prompt)
            result = query_sql(sql_query)

            if result and isinstance(result[0], (list, tuple)):
                answer = result[0][0]
            else:
                answer = "No result found."
        except Exception as e:
            traceback.print_exc()
            answer = f"Error: {e}"
            sql_query = "N/A"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "answer": answer,
        "sql": sql_query
    })
