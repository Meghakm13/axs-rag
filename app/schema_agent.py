# app/schema_agent.py

from typing import Any, Dict, List


FULL_SCHEMA = {
    "customers": ["id", "name", "city", "created_at"],
    "employees": ["id", "name", "role", "hired_at"],
    "products": ["id", "name", "category", "price"],
    "orders": ["id", "customer_id", "employee_id", "order_date", "total_amount"],
    "order_items": ["id", "order_id", "product_id", "quantity", "line_total"],
}

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
    "sales": ["orders"],
    "amount": ["orders"],
    "total": ["orders"],
}


def get_relevant_schema(question: str) -> Dict[str, Any]:
    q = question.lower()
    tables: List[str] = []

    for keyword, mapped_tables in KEYWORDS_TO_TABLES.items():
        if keyword in q:
            for t in mapped_tables:
                if t not in tables:
                    tables.append(t)

    if not tables:
        tables = ["orders"]

    columns = {table: FULL_SCHEMA[table] for table in tables if table in FULL_SCHEMA}

    return {
        "tables": tables,
        "columns": columns,
    }
