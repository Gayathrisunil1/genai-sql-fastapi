# 🧠 GenAI-SQL-FastAPI

This project allows users to ask natural language questions about e-commerce data. It converts them into SQL queries using **Google's Gemini model**, runs the queries on a **SQLite database**, and displays the results using **FastAPI** — with clear **tables** and interactive **charts**.

---

### 🚀 Features

- ✨ Natural language to SQL conversion  
- 🧠 Uses Google Gemini API  
- ⚡ FastAPI-based backend  
- 📋 Displays SQL results in a clean **table view**  
- 📊 Generates dynamic **bar charts** with Chart.js  
- 🗂️ Works with e-commerce datasets like:
  - `total_sales.csv`
  - `ad_sales.csv`
  - `eligibility.csv`

---

### 🛠️ Setup Instructions

1. **Clone this repo**
2. **Create a virtual environment and install dependencies**:


python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt

Run the app:
uvicorn main:app --reload

💬 Example Questions You Can Ask
What is the total ad sales per item?
How many units were sold on 2024-11-10?
Show me the average ad spend by date.

📸 Usage Example
When you ask:

"What is the total ad sales per item?"

You get:

✅ Table View:
item_id	total_ad_sales
0	₹6,945.00
1	₹2,127.16
2	₹2,636.14
...	...

📊 Bar Chart:

📦 Folder Structure
genai-sql-fastapi/
├── main.py
├── templates/
│   └── index.html
├── static/
├── requirements.txt
└── README.md



