# app/sql_generator_agent.py

from typing import Dict, Any, List, Tuple
import re


# Cities 
KNOWN_CITIES = [
    "mumbai",
    "delhi",
    "bengaluru",
    "pune",
    "ahmedabad",
    "chennai",
    "hyderabad",
    "jaipur",
    "nagpur",
    "kolkata",
]


def _detect_city(question: str) -> str | None:
    q = question.lower()
    for city in KNOWN_CITIES:
        if city in q:
            # Capitalize 
            return city.capitalize()
    return None


def _detect_amount_threshold(question: str) -> float | None:
    """
    Detect phrases like:
      - greater than 20000
      - more than 50000
      - above 10000
    Returns the numeric value if found.
    """
    q = question.lower()
    match = re.search(r"(greater than|more than|above)\s+(\d+)", q)
    if match:
        return float(match.group(2))
    return None


def _detect_year(question: str) -> int | None:
    """
    Detect explicit year like 2023, 2024...
    """
    match = re.search(r"(20\d{2})", question)
    if match:
        return int(match.group(1))
    return None


def _build_time_filter(question: str, alias: str = "o") -> str:
    """
    Build a WHERE condition for time windows based on certain phrases.
    Uses PostgreSQL date functions.
    """
    q = question.lower()
    conditions: List[str] = []

    if "last year" in q:
        conditions.append(
            f"{alias}.order_date >= date_trunc('year', current_date) - interval '1 year'"
        )
        conditions.append(
            f"{alias}.order_date < date_trunc('year', current_date)"
        )
    elif "this year" in q or "current year" in q:
        conditions.append(
            f"{alias}.order_date >= date_trunc('year', current_date)"
        )
        conditions.append(
            f"{alias}.order_date < date_trunc('year', current_date) + interval '1 year'"
        )
    elif "last month" in q:
        conditions.append(
            f"{alias}.order_date >= date_trunc('month', current_date) - interval '1 month'"
        )
        conditions.append(
            f"{alias}.order_date < date_trunc('month', current_date)"
        )
    elif "this month" in q or "current month" in q:
        conditions.append(
            f"{alias}.order_date >= date_trunc('month', current_date)"
        )
        conditions.append(
            f"{alias}.order_date < date_trunc('month', current_date) + interval '1 month'"
        )
    else:
        # Year specified
        year = _detect_year(q)
        if year:
            conditions.append(f"{alias}.order_date >= DATE '{year}-01-01'")
            conditions.append(f"{alias}.order_date < DATE '{year+1}-01-01'")

    if not conditions:
        return ""

    return " AND ".join(conditions)


def generate_sql(question: str, schema_info: Dict[str, Any]) -> str:
    """
    SQL Generator Agent.

    Supported patterns (for now):
    - How many orders ... ?
    - How many customers ... ?
    - Total / sum revenue from orders
    - Filters:
        - by city (Mumbai, Delhi, etc.)
        - by amount (greater than / more than / above X)
        - by time (last year, this year, last month, this month, in 2023, etc.)
    """
    q = question.lower()
    tables = schema_info.get("tables", [])

    # ---------------------------
    # Detect context
    # ---------------------------
    has_orders = "order" in q or "orders" in q or "orders" in tables
    has_customers = "customer" in q or "customers" in q or "customers" in tables

    city = _detect_city(q)
    amount_threshold = _detect_amount_threshold(q)
    time_filter_expr = _build_time_filter(q, alias="o")

    # ---------------------------
    # 1) "How many ..." style questions
    # ---------------------------
    if "how many" in q or "number of" in q:
        # How many orders?
        if has_orders:
            base = "SELECT COUNT(*) AS count FROM orders o"
            where_clauses: List[str] = []

            # If city mentioned, join customers
            if city:
                base += " JOIN customers c ON c.id = o.customer_id"
                where_clauses.append(f"c.city = '{city}'")

            # Amount filter
            if amount_threshold is not None:
                where_clauses.append(f"o.total_amount > {amount_threshold}")

            # Time filter
            if time_filter_expr:
                where_clauses.append(time_filter_expr)

            if where_clauses:
                return base + " WHERE " + " AND ".join(where_clauses) + ";"
            else:
                return base + ";"

        # How many customers?
        if has_customers:
            base = "SELECT COUNT(*) AS count FROM customers c"
            where_clauses: List[str] = []

            if city:
                where_clauses.append(f"c.city = '{city}'")

            if where_clauses:
                return base + " WHERE " + " AND ".join(where_clauses) + ";"
            else:
                return base + ";"

    # ---------------------------
    # 2) Total / sum revenue
    # ---------------------------
    if ("total" in q or "sum" in q or "revenue" in q or "sales" in q) and has_orders:
        base = "SELECT SUM(o.total_amount) AS total_amount FROM orders o"
        where_clauses: List[str] = []

        if city:
            base += " JOIN customers c ON c.id = o.customer_id"
            where_clauses.append(f"c.city = '{city}'")

        if amount_threshold is not None:
            where_clauses.append(f"o.total_amount > {amount_threshold}")

        if time_filter_expr:
            where_clauses.append(time_filter_expr)

        if where_clauses:
            return base + " WHERE " + " AND ".join(where_clauses) + ";"
        else:
            return base + ";"

    # ---------------------------
    # 3) Generic "show me orders" style
    # ---------------------------
    if has_orders:
        base = "SELECT o.* FROM orders o"
        where_clauses: List[str] = []

        if city:
            base += " JOIN customers c ON c.id = o.customer_id"
            where_clauses.append(f"c.city = '{city}'")

        if amount_threshold is not None:
            where_clauses.append(f"o.total_amount > {amount_threshold}")

        if time_filter_expr:
            where_clauses.append(time_filter_expr)

        sql = base
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
        sql += " ORDER BY o.order_date DESC LIMIT 10;"

        return sql

    # ---------------------------
    # 4) Fallbacks for customers
    # ---------------------------
    if has_customers:
        base = "SELECT * FROM customers c"
        where_clauses: List[str] = []

        if city:
            where_clauses.append(f"c.city = '{city}'")

        sql = base
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
        sql += " ORDER BY c.created_at DESC LIMIT 10;"

        return sql

    # ---------------------------
    # Final fallback
    # ---------------------------
    raise ValueError("Unable to generate SQL for this question yet.")
