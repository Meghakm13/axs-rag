# app/sql_generator_agent.py

from typing import Dict, Any


def generate_sql(question: str, schema_info: Dict[str, Any]) -> str:
    """
    Very basic 'SQL Generator Agent'.
    For Block 2, we only handle a couple of patterns.
    We'll add more patterns (filters, dates, etc.) in the next block.
    """
    q = question.lower()
    tables = schema_info.get("tables", [])

    # Pattern 1: how many orders
    if "how many" in q and "order" in q:
        return "SELECT COUNT(*) AS count FROM orders;"

    # Pattern 2: how many customers
    if "how many" in q and "customer" in q:
        return "SELECT COUNT(*) AS count FROM customers;"

    # Simple fallback: if orders table is involved and no special phrasing
    if "orders" in tables:
        return "SELECT * FROM orders LIMIT 10;"

    # Fallback: just show first 10 customers
    if "customers" in tables:
        return "SELECT * FROM customers LIMIT 10;"

    # If still nothing, raise error so /ask can handle it
    raise ValueError("Unable to generate SQL for this question yet.")
