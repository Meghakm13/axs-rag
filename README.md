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
│   ├── main.py                 # FastAPI backend
│   ├── config.py               # DB credentials
│   ├── db.py                   # DB connector
│   ├── schema_agent.py         # Agent 1
│   ├── sql_generator_agent.py  # Agent 2
│   ├── retriever_agent.py      # Agent 3
│   ├── synthesizer_agent.py    # Agent 4
│   ├── knowledge_base.py       # Bonus: doc-based fallback
│   └── models.sql              # Schema + sample data
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
Follow these steps to run the backend API and frontend UI.

## **Step 1 — Clone the project**

```bash
git clone <your-repo-url>
cd axs-rag-assignment
```

---

## **Step 2 — Create a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate
```

---

## **Step 3 — Install dependencies**

```bash
pip install -r requirements.txt
```

---

## **Step 4 — Setup PostgreSQL Database**

1. Open PostgreSQL (psql or pgAdmin).
2. Create a new database:

```sql
CREATE DATABASE axs_assignment;
```

3. Load the schema + sample Indian data:

```bash
psql -U postgres -d axs_assignment -f app/models.sql
```

4. Update your PostgreSQL **username** and **password** inside:

```
app/config.py
```

---

## **Step 5 — Run Backend + Frontend Together (`runall.py`)**

run **runall.py** file to start both servers at once.

```bash
python runall.py
```

This will automatically:

* Start **FastAPI backend** at → `http://127.0.0.1:8000`
* Start **Frontend UI** at → `http://127.0.0.1:5500/index.html`
* Open the UI in your browser

---

## **Step 6 — Test Everything**

### Backend health check:

```
http://127.0.0.1:8000/health
```

### API docs:

```
http://127.0.0.1:8000/docs
```

### Frontend UI:

```
http://127.0.0.1:5500/index.html
```

---

## ⭐ 6. Bonus: Document-Based Knowledge Fallback

If the SQL Generator cannot handle a question:

The system falls back to a document-based knowledge store (in-memory)

Provides explanatory answers using internal notes

Implemented in: app/knowledge_base.py

---

## 🧭 7. Future Improvements

* Use LLM for generating SQL instead of rule-based agent
* Vector embeddings for schema understanding
* More advanced NLP parsing
* Security checks against SQL injection
* Pagination for result sets
* Authentication for API
