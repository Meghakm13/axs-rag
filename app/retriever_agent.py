# app/retriever_agent.py

from typing import List, Dict, Any
from .db import get_connection


def run_query(sql: str) -> List[Dict[str, Any]]:
    """
    'Retriever Agent':
    - Executes the SQL on PostgreSQL
    - Returns rows as list of dictionaries
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()  
        cur.close()
        return list(rows)
    finally:
        conn.close()
