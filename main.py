import sqlite3
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ask Gemini to generate SQL
def ask_gemini(prompt):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    text = response.text.strip()

    # Clean up markdown and extract only SQL
    if "```sql" in text:
        text = text.split("```sql")[1]
    elif "```" in text:
        text = text.split("```")[1]

    text = text.replace("```", "").strip()

    sql_lines = []
    for line in text.splitlines():
        if any(word in line.lower() for word in ["select", "from", "where", "group by", "order by", "limit", "sum", "avg", "as"]):
            sql_lines.append(line)

    clean_sql = "\n".join(sql_lines).strip()
    print("Cleaned SQL:", clean_sql)
    return clean_sql

# Run SQL and return result
def query_sql(sql):
    conn = sqlite3.connect("ecom.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    result = cursor.fetchall()
    conn.close()
    return result, columns

# Home Route: GET + POST
@app.get("/", response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
async def home(request: Request):
    answer = None
    sql_query = None
    labels = []
    values = []
    show_chart = False
    columns = []
    result = []  # ✅ Add this to fix the internal server error

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
            result, columns = query_sql(sql_query)

            if result and isinstance(result[0], tuple) and len(result[0]) == 2:
                labels = [str(row[0]) for row in result]
                values = [float(row[1]) for row in result]
                show_chart = True
                answer = "\n".join(
                    [f"{columns[0]}: {row[0]} → {columns[1]}: ₹{row[1]:,.2f}" for row in result]
                )
            else:
                answer = result[0][0] if result else "No result found."

        except Exception as e:
            answer = f"Error: {e}"
            sql_query = "N/A"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "answer": answer,
        "sql": sql_query,
        "labels": labels,
        "values": values,
        "show_chart": show_chart,
        "columns": columns,
        "result": result  # ✅ Now this will always be defined
    })

