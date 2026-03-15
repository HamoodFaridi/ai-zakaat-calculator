import sqlite3
from datetime import datetime

DB_NAME = "zakaat.db"
SCHEMA_VERSION = 1

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Metadata table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metadata (
        key TEXT PRIMARY KEY,
        value TEXT
    )               
    """)

    cursor.execute("SELECT value FROM metadata WHERE key='schema_version'")
    row = cursor.fetchone()
    if row is None:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS zakaat_records(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER UNIQUE,
            date TEXT,
            cash REAL,
            gold_value REAL,
            silver_value REAL,
            investments REAL,
            business_assets REAL,
            rental_savings REAL,
            loans REAL,
            debts REAL,
            total_assets REAL,
            nisab_threshold REAL,
            zakat_due REAL,
            currency TEXT
        )
        """)

        cursor.execute("""
        INSERT INTO metadata (key, value)
        VALUES ('schema_version', ?)
        """, (SCHEMA_VERSION,))
    conn.commit()
    conn.close()


    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS zakaat_records (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     date TEXT,
    #     cash REAL,
    #     gold_value REAL,
    #     silver_value REAL,
    #     investments REAL,
    #     business_assets REAL,
    #     rental_savings REAL,
    #     loans REAL,
    #     debts REAL,
    #     total_assets REAL,
    #     nisab_threshold REAL,
    #     zakat_due REAL,
    #     currency TEXT
    # )
    # """)
    # conn.commit()
    # conn.close()

def save_record(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO zakaat_records (
        year, date, cash, gold_value, silver_value, investments,
        business_assets, rental_savings, loans, debts,
        total_assets, nisab_threshold, zakat_due, currency
    )   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["year"],
        datetime.now().strftime("%Y-%m-%d"),
        data["cash"],
        data["gold"],
        data["silver"],
        data["investments"],
        data["business"],
        data["rental"],
        data["loans"],
        data["debts"],
        data["total_assets"],
        data["nisab_threshold"],
        data["zakat_due"],
        data["currency"]
    ))
    # cursor.execute("""
    # INSERT INTO zakaat_records (
    #     date, cash, gold_value, silver_value, investments,
    #     business_assets, rental_savings, loans, debts,
    #     total_assets, nisab_threshold, zakat_due, currency
    # )   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    # """, (
    #     datetime.now().strftime("%Y-%m-%d"),
    #     data["cash"],
    #     data["gold"],
    #     data["silver"],
    #     data["investments"],
    #     data["business"],
    #     data["rental"],
    #     data["loans"],
    #     data["debts"],
    #     data["total_assets"],
    #     data["nisab_threshold"],
    #     data["zakat_due"],
    #     data["currency"]
    # ))

    conn.commit()
    conn.close()

def get_records():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM zakaat_records ORDER BY year DESC")

    records = cursor.fetchall()
    conn.close()
    
    return records