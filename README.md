# 📘 NL → SQL Multi-Agent System

### Convert Natural Language Questions → SQL Queries → Database Answers

## 📝 1. Overview

This project implements a **multi-agent pipeline** that converts **natural language questions** into **PostgreSQL queries**, executes them, and returns a **human-readable answer**.

The system supports:

* Counting 
* Aggregations 
* Filters 
* Time-based phrases 
* Joins between customers, orders, employees, etc.

Frontend: simple web UI.
Backend: FastAPI.
Database: PostgreSQL with mock business data.

---

## 🧩 2. Architecture

### 🔄 Multi-Agent Flow

```
User Question
      ↓
1) Schema Agent → Identify relevant tables & columns
      ↓
2) SQL Generator Agent → Convert question → SQL
      ↓
3) Retriever Agent → Execute SQL on PostgreSQL
      ↓
4) Synthesizer Agent → Convert rows → Human Answer
      ↓
Final Response (JSON + UI)
```

### 🧠 Agents

| Agent                   | Responsibility                                                |
| ----------------------- | ------------------------------------------------------------- |
| **Schema Agent**        | Finds which tables/columns are relevant using keyword mapping |
| **SQL Generator Agent** | Creates SQL queries using rule-based NLP patterns             |
| **Retriever Agent**     | Executes SQL safely on PostgreSQL and returns rows            |
| **Synthesizer Agent**   | Converts raw rows to clear, readable English answers          |

---

## 🗂️ 3. Project Structure

```
axs-rag-assignment/
├── app/
│   ├── main.py                 # FastAPI app & routes
│   ├── config.py               # DB config
│   ├── db.py                   # DB connection helper
│   ├── schema_agent.py         # Agent 1
│   ├── sql_generator_agent.py  # Agent 2
│   ├── retriever_agent.py      # Agent 3
│   ├── synthesizer_agent.py    # Agent 4
│   ├── models.sql              # PostgreSQL schema & sample Indian data
│
├── web/
│   ├── index.html              # Frontend UI
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🗄️ 4. Database Schema (PostgreSQL)

The database contains context data (names, cities, INR values).

### 🧱 Tables

* **customers**
  `id, name, city, created_at`

* **employees**
  `id, name, role, hired_at`

* **products**
  `id, name, category, price`

* **orders**
  `id, customer_id, employee_id, order_date, total_amount`

* **order_items**
  `id, order_id, product_id, quantity, line_total`

### 📦 Sample Rows

100+ rows of business data:

* Cities: Mumbai, Delhi, Bengaluru, Pune, Chennai, Hyderabad, Kolkata, etc.
* Prices in ₹ (INR)
* Time coverage across 2023–2024 for time-based queries

---

## 🚀 5. Setup Instructions

### 5.1 Prerequisites

* Python 3.10+
* PostgreSQL (running locally)
* pip / virtualenv
* Git

---

### 5.2 Running the System

Clone the repository:
git clone <repo-url> && cd axs-rag-assignment

Set up a virtual environment and install dependencies from requirements.txt.

Create a PostgreSQL database (e.g. axs_assignment) and apply app/models.sql.

Configure credentials in app/config.py.

Start the backend with Uvicorn and open the API docs at /docs.

Optionally serve web/index.html via a simple static server and interact with /ask from the browser.

```bash
git clone <your-repo-url>
cd axs-rag-assignment

python -m venv venv
venv\Scripts\activate       # Windows
# or
source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

## 🧭 6. Future Improvements

* Use LLM for generating SQL instead of rule-based agent
* Vector embeddings for schema understanding
* More advanced NLP parsing
* Security checks against SQL injection
* Pagination for result sets
* Authentication for API
* Deploy backend + frontend on cloud (Render/Netlify)
* Create a more professional header section with a logo-style ASCII banner
* Proofread your README for interview polish
