# app/schema_agent.py

from typing import Any, Dict, List


# Simple schema description for our DB
FULL_SCHEMA = {
    "customers": ["id", "name", "city", "created_at"],
    "employees": ["id", "name", "role", "hired_at"],
    "products": ["id", "name", "category", "price"],
    "orders": ["id", "customer_id", "employee_id", "order_date", "total_amount"],
    "order_items": ["id", "order_id", "product_id", "quantity", "line_total"],
}

# Map keywords in question → tables
KEYWORDS_TO_TABLES = {
    "customer": ["customers"],
    "customers": ["customers"],
    "order": ["orders", "order_items"],
    "orders": ["orders", "order_items"],
    "employee": ["employees"],
    "employees": ["employees"],
    "product": ["products"],
    "products": ["products"],
    "city": ["customers"],
    "revenue": ["orders"],
    "sale": ["orders"],
}


def get_relevant_schema(question: str) -> Dict[str, Any]:
    """
    Very simple 'Schema Agent':
    - Looks at keywords in the question
    - Returns the tables and their columns that might be used
    """
    q = question.lower()
    tables: List[str] = []

    # pick tables based on keywords
    for keyword, mapped_tables in KEYWORDS_TO_TABLES.items():
        if keyword in q:
            for t in mapped_tables:
                if t not in tables:
                    tables.append(t)

    # fallback: if no keyword found, assume orders
    if not tables:
        tables = ["orders"]

    # Build columns info for the selected tables
    columns = {table: FULL_SCHEMA[table] for table in tables if table in FULL_SCHEMA}

    return {
        "tables": tables,
        "columns": columns,
    }
