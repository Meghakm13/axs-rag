# app/knowledge_base.py

from typing import List, Dict
import re

# Tiny internal knowledge base.
# You can put things like: how the system works, what certain metrics mean, etc.
DOCUMENTS: List[Dict[str, str]] = [
    {
        "id": "kb-1",
        "title": "What data does this system use?",
        "content": (
            "The system uses business data with customers, "
            "employees, products, orders, and order_items stored in PostgreSQL. "
            "Orders cover the years 2023 and 2024."
        ),
    },
    {
        "id": "kb-2",
        "title": "What is total_amount in orders?",
        "content": (
            "The total_amount column in the orders table represents the total "
            "order value in Indian Rupees (₹), aggregated from all order_items."
        ),
    },
    {
        "id": "kb-3",
        "title": "What can I ask this system?",
        "content": (
            "You can ask about number of orders, total revenue, customers in a city, "
            "large orders above a threshold, and time-based ranges like last year or this month."
        ),
    },
    {
        "id": "kb-4",
        "title": "Limitations of the system",
        "content": (
            "The SQL generation is rule-based and supports only a subset of English queries. "
            "Very complex or ambiguous questions may not work and will return an error."
        ),
    },
]


def search_knowledge(question: str, top_k: int = 1) -> List[Dict[str, str]]:
    """
    Very simple keyword-based search over DOCUMENTS.
    - Splits question into words
    - Scores each document by how many words match
    - Returns top_k documents with score > 0
    """
    q = question.lower()
    # Basic word tokens (remove super short words)
    words = [w for w in re.findall(r"\w+", q) if len(w) > 3]

    scored: List[tuple[int, Dict[str, str]]] = []
    for doc in DOCUMENTS:
        text = (doc["title"] + " " + doc["content"]).lower()
        score = sum(1 for w in words if w in text)
        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored[:top_k]]
