# 🧠 GenAI-SQL-FastAPI

This project allows users to ask natural language questions about e-commerce data, and it converts them into SQL queries using Google's Gemini model, then runs them on a SQLite database using FastAPI.

## 🚀 Features
- ✨ Natural language to SQL conversion
- 🧠 Uses Google Gemini API
- 📦 FastAPI-based backend
- 📊 Works with e-commerce datasets like `total_sales.csv`, `ad_sales.csv`, and `eligibility.csv`

## 🛠 Setup Instructions
1. Clone this repo
2. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
