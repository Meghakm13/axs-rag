# app/synthesizer_agent.py

from typing import List, Dict, Any


def generate_answer(question: str, rows: List[Dict[str, Any]]) -> str:
    """
    Synthesizer Agent:
    - If aggregate COUNT: say "There are X ..."
    - If aggregate SUM(total_amount): say "Total revenue is ₹X ..."
    - Otherwise: show up to 5 rows in a simple text format.
    """
    if not rows:
        return "No matching records were found for your question."

    # Single-row aggregates
    row0 = rows[0]

    # 1) COUNT aggregate
    if len(rows) == 1 and "count" in row0:
        count_value = row0["count"]
        return f"There are {count_value} records matching your question."

    # 2) SUM(total_amount) aggregate
    if len(rows) == 1 and "total_amount" in row0:
        total = row0["total_amount"]
        try:
            # format like ₹12,34,567.89 with commas
            total_num = float(total)
            total_str = f"₹{total_num:,.2f}"
        except Exception:
            total_str = f"₹{total}"
        return f"The total revenue matching your question is {total_str}."

    # 3) Generic listing
    preview_rows = rows[:5]  
    lines = ["Here are some matching records (showing up to 5):"]

    for idx, row in enumerate(preview_rows, start=1):
        pieces = [f"{k}={v}" for k, v in row.items()]
        line = f"{idx}. " + ", ".join(pieces)
        lines.append(line)

    if len(rows) > 5:
        lines.append(f"...and {len(rows) - 5} more rows not shown.")

    return "\n".join(lines)
