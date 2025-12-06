# app/synthesizer_agent.py

from typing import List, Dict, Any


def generate_answer(question: str, rows: List[Dict[str, Any]]) -> str:
    """
    'Synthesizer Agent':
    - Takes question + result rows
    - Returns a human-readable string answer
    For now, very basic handling for:
      - Count queries (one row with 'count')
      - Generic listing (show first few rows)
    """
    if not rows:
        return "No matching records were found for your question."

    # If looks like an aggregate: one row, has a 'count' column
    if len(rows) == 1 and "count" in rows[0]:
        count_value = rows[0]["count"]
        return f"There are {count_value} records matching your question."

    # Otherwise, generic listing
    preview_rows = rows[:5]  # show at most 5 rows
    lines = ["Here are some matching records (showing up to 5):"]

    for idx, row in enumerate(preview_rows, start=1):
        # Build a simple "key=value" joined string for each row
        pieces = [f"{k}={v}" for k, v in row.items()]
        line = f"{idx}. " + ", ".join(pieces)
        lines.append(line)

    if len(rows) > 5:
        lines.append(f"...and {len(rows) - 5} more rows not shown.")

    return "\n".join(lines)
