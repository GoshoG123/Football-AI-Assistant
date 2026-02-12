import sqlite3

DB_FILE = "database.db"
SCHEMA_FILE = "schema.sql"

def create_database():
    with sqlite3.connect(DB_FILE) as conn:
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
    print("✅ Базата е създадена успешно с тестовите данни!")

def show_table(table_name):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        print(f"\n📋 Table: {table_name} ({len(rows)} rows)")
        for row in rows:
            print(dict(row))

tables = [
    "clubs",
    "players",
    "transfers",
    "leagues",
    "league_teams",
    "matches",
    "goals",
    "cards"
]

if __name__ == "__main__":
    create_database()

    for table in tables:
        show_table(table)
