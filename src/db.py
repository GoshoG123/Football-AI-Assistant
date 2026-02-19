import sqlite3
import os

# Пътища
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) 
SQL_DIR = os.path.join(BASE_DIR, "sql")     
DB_FILE = os.path.join(SQL_DIR, "database.db")
SCHEMA_FILE = os.path.join(SQL_DIR, "schema.sql")


# Връзка към базата
def get_connection():
    """
    Връща sqlite3 връзка към database.db с Row factory
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # позволява достъп по име на колона
        return conn
    except sqlite3.Error as e:
        print("Database connection error:", e)
        return None


# Инициализация на базата
def init_db():
    """
    Създава базата (database.db) и всички таблици от schema.sql
    """
    if not os.path.exists(SQL_DIR):
        os.makedirs(SQL_DIR)

    try:
        conn = get_connection()
        if conn is None:
            print("Failed to create database connection.")
            return

        if not os.path.exists(SCHEMA_FILE):
            print(f"Error: {SCHEMA_FILE} not found!")
            return

        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            conn.executescript(f.read())

        conn.commit()
        conn.close()
        print(f"✅ Database created successfully at {DB_FILE}!")

    except Exception as e:
        print("Database initialization error:", e)


# Автоматично създаване на базата при стартиране на db.py
if __name__ == "__main__":
    init_db()
