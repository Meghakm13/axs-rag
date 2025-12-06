# app/main.py

from .schema_agent import get_relevant_schema
from .sql_generator_agent import generate_sql
from .retriever_agent import run_query
from .synthesizer_agent import generate_answer
from .db import get_connection
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

# ---------- FastAPI app setup ----------
app = FastAPI(
    title="AXS RAG Assignment API",
    description="Simple multi-agent pipeline for NL → SQL → Answer",
    version="0.1.0",
)

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins (ok for assignment)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ---------- Request & Response Models ----------

class AskRequest(BaseModel):
    question: str


class IntermediateResult(BaseModel):
    relevant_schema: Dict[str, Any] = {}
    sql_query: str = ""
    result_rows: List[Dict[str, Any]] = []


class AskResponse(BaseModel):
    answer: str
    intermediate: IntermediateResult
    error: Optional[str] = None


# ---------- Basic health check ----------

@app.get("/health")
def health_check():
    return {"status": "ok"}

# ---------- Database connectivity test ----------
@app.get("/test-db")
def test_db():
    """
    Simple endpoint to confirm DB connectivity and sample data.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) AS customer_count FROM customers;")
        row = cur.fetchone()
        cur.close()
        conn.close()
        return {
            "db_status": "ok",
            "customer_count": row["customer_count"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# ---------- /ask endpoint ----------

@app.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest):
    """
    Main pipeline:
    1. Schema Agent -> identify relevant tables/columns
    2. SQL Generator Agent -> build SQL query
    3. Retriever Agent -> execute SQL and get rows
    4. Synthesizer Agent -> turn rows into human answer
    """
    question = payload.question
    intermediate = IntermediateResult()

    try:
        # 1) Schema Agent
        schema_info = get_relevant_schema(question)
        intermediate.relevant_schema = schema_info

        # 2) SQL Generator Agent
        sql_query = generate_sql(question, schema_info)
        intermediate.sql_query = sql_query

        # 3) Retriever Agent
        result_rows = run_query(sql_query)
        intermediate.result_rows = result_rows

        # 4) Synthesizer Agent
        answer = generate_answer(question, result_rows)

        return AskResponse(
            answer=answer,
            intermediate=intermediate,
            error=None,
        )

    except ValueError as ve:
        # Typically from SQL generator when it can't handle the question
        return AskResponse(
            answer="",
            intermediate=intermediate,
            error=str(ve),
        )
    except Exception as e:
        # Any unexpected errors (DB issues, bugs, etc.)
        # In real app you would log this.
        raise HTTPException(status_code=500, detail=str(e))

