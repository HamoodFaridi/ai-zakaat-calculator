import sqlite3
from datetime import datetime

DB_NAME = "zakaat.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS zakaat_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        cash REAL,
        investments REAL,
        gold_value REAL,
        silver_value REAL,
        business_assets REAL,
        rental_savings REAL,
        debts REAL,
        loans REAL,
        total_assets REAL,
        nisab_threshold REAL,
        zakaat_due REAL,
        currency TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_record(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO zakaat_records (
        date, cash, investments, gold_value, silver_value,
        business_assets, rental_savings, debts, loans,
        total_assets, nisab_threshold, zakaat_due, currency
    )   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d"),
        data["cash"],
        data["investments"],
        data["gold"],
        data["silver"],
        data["business"],
        data["rental"],
        data["debts"],
        data["loans"],
        data["total"],
        data["nisab"],
        data["zakaat"],
        data["currency"]
    ))

    conn.commit()
    conn.close()

def get_records():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.row_factory = sqlite3.Row

    cursor.execute("SELECT * FROM zakaat_records ORDER BY date DESC")

    records = cursor.fetchall()
    conn.close()
    
    return records