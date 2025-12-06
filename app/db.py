# app/db.py

import psycopg2
from psycopg2.extras import RealDictCursor
from .config import DB_CONFIG


def get_connection():
    """
    Create and return a new database connection.
    Caller is responsible for closing it.
    """
    conn = psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        cursor_factory=RealDictCursor,  # rows as dicts
    )
    return conn
