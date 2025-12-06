# app/main.py

from .db import get_connection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

app = FastAPI(
    title="AXS RAG Assignment API",
    description="Simple multi-agent pipeline for NL → SQL → Answer",
    version="0.1.0",
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



# ---------- Dummy /ask endpoint ----------

@app.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest):
    """
    Block 0: Just return a dummy response.
    Later we will plug in:
      - Schema Agent
      - SQL Generator Agent
      - Retriever Agent
      - Synthesizer Agent
    """
    # For now, we don't do any real logic.
    dummy_intermediate = IntermediateResult(
        relevant_schema={},
        sql_query="-- SQL will appear here in later blocks",
        result_rows=[],
    )

    return AskResponse(
        answer="This is a dummy answer. The real pipeline will be added in the next blocks.",
        intermediate=dummy_intermediate,
        error=None,
    )
