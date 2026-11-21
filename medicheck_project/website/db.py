"""
Database connection helper for MediCheck.
Supports PostgreSQL (when configured) and automatically falls back to
SQLite with auto-seeding so the web application is 100% functional out of the box.
"""
import os
import sys
import re
import sqlite3

USE_PG = False
PG_MODULE = None

try:
    import psycopg2
    import psycopg2.extras
    PG_MODULE = psycopg2
except ImportError:
    PG_MODULE = None

DB_FILE = os.path.join(os.path.dirname(__file__), "medicheck.db")


def check_pg_connection():
    global USE_PG
    if not PG_MODULE:
        return False
    try:
        conn = PG_MODULE.connect(
            dbname=os.environ.get("DB_NAME", "medicheck"),
            user=os.environ.get("DB_USER", "postgres"),
            password=os.environ.get("DB_PASSWORD", "postgres"),
            host=os.environ.get("DB_HOST", "localhost"),
            port=os.environ.get("DB_PORT", "5432"),
            connect_timeout=2
        )
        conn.close()
        return True
    except Exception:
        return False


USE_PG = check_pg_connection()


def get_sqlite_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_sqlite_db(force_recreate=False):
    """Build SQLite tables and insert seed data if medicheck.db is missing or empty."""
    if force_recreate and os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
        except Exception:
            pass

    conn = get_sqlite_conn()
    cursor = conn.cursor()
    
    # Check if patients table exists and has data
    try:
        cursor.execute("SELECT COUNT(*) FROM patients;")
        count = cursor.fetchone()[0]
        if count > 0 and not force_recreate:
            conn.close()
            return
    except sqlite3.OperationalError:
        pass  # Table doesn't exist yet

    print("Initializing SQLite database with schema and seed data...")

    proj_dir = os.path.dirname(os.path.dirname(__file__))
    schema_path = os.path.join(proj_dir, "database", "schema.sql")
    seed_path = os.path.join(proj_dir, "database", "seed_data.sql")

    if not os.path.exists(schema_path):
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    if not os.path.exists(seed_path):
        seed_path = os.path.join(os.path.dirname(__file__), "seed_data.sql")

    if os.path.exists(schema_path):
        with open(schema_path, "r", encoding="utf-8") as f:
            sql = f.read()
        
        # Remove single-line comments
        sql = re.sub(r"--.*$", "", sql, flags=re.MULTILINE)
        
        # Convert multi-table DROP TABLE IF EXISTS ... CASCADE; into individual DROP statements
        def fix_drop(match):
            tables = match.group(1).split(",")
            return "; ".join([f"DROP TABLE IF EXISTS {t.strip()}" for t in tables]) + ";"

        sql = re.sub(r"DROP TABLE IF EXISTS\s+(.*?)\s+CASCADE;", fix_drop, sql, flags=re.IGNORECASE | re.DOTALL)
        
        # Clean Postgres specific type SERIAL (SQLite accepts CURRENT_DATE as DEFAULT naturally)
        sql = sql.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
        
        statements = [s.strip() for s in sql.split(";") if s.strip()]
        for stmt in statements:
            try:
                cursor.execute(stmt)
            except Exception as e:
                print(f"Schema stmt error: {e} | stmt snippet: {stmt[:60]}")

    if os.path.exists(seed_path):
        with open(seed_path, "r", encoding="utf-8") as f:
            sql = f.read()
        
        sql = re.sub(r"--.*$", "", sql, flags=re.MULTILINE)
        sql = re.sub(r"SELECT setval\(.*?\);", "", sql, flags=re.IGNORECASE)
        
        statements = [s.strip() for s in sql.split(";") if s.strip()]
        for stmt in statements:
            try:
                cursor.execute(stmt)
            except Exception as e:
                print(f"Seed stmt error: {e} | stmt snippet: {stmt[:60]}")

    conn.commit()
    conn.close()
    print("SQLite database initialized successfully with full tables and seed data!")


if not USE_PG:
    try:
        init_sqlite_db(force_recreate=False)
    except Exception as e:
        print(f"DB Init error: {e}")


def query(sql, params=None, fetch=True, commit=False):
    """Run a parameterized query across PostgreSQL or SQLite."""
    if USE_PG:
        conn = PG_MODULE.connect(
            dbname=os.environ.get("DB_NAME", "medicheck"),
            user=os.environ.get("DB_USER", "postgres"),
            password=os.environ.get("DB_PASSWORD", "postgres"),
            host=os.environ.get("DB_HOST", "localhost"),
            port=os.environ.get("DB_PORT", "5432"),
        )
        try:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(sql, params or ())
            result = cur.fetchall() if fetch else None
            if commit:
                conn.commit()
            return result
        finally:
            conn.close()
    else:
        conn = get_sqlite_conn()
        try:
            cur = conn.cursor()
            sqlite_sql = sql
            sqlite_sql = re.sub(r"string_agg\((.*?), (.*?)\)", r"group_concat(\1, \2)", sqlite_sql, flags=re.IGNORECASE)
            sqlite_sql = re.sub(r"date_trunc\('month',\s*(.*?)\)", r"strftime('%Y-%m', \1)", sqlite_sql, flags=re.IGNORECASE)
            sqlite_sql = sqlite_sql.replace("CURRENT_DATE", "DATE('now')")
            sqlite_sql = sqlite_sql.replace("%s", "?")

            cur.execute(sqlite_sql, params or ())
            
            result = None
            if fetch:
                rows = cur.fetchall()
                result = [dict(row) for row in rows]
            elif "RETURNING" in sql.upper():
                rows = cur.fetchall()
                result = [dict(row) for row in rows]

            if commit:
                conn.commit()
            return result
        finally:
            conn.close()
