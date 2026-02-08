import sqlite3

# Име на SQLite база
DB_FILE = "database.db"

# Таблиците в реда, в който трябва да се изтриват и създават
tables = [
    "cards", "goals", "matches", "league_teams", "leagues",
    "transfers", "players", "clubs"
]

# 1️⃣ Свързване с базата
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
print("🔹 Connected to database.")

# 2️⃣ DROP TABLE IF EXISTS за всички таблици (за многократно пускане)
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table};")
print("🔹 Old tables dropped (if existed).")

# 3️⃣ Зареждане на schema.sql
with open("schema.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

cursor.executescript(sql_script)
print("✅ Tables created and sample data inserted!")

# 4️⃣ Функция за показване на съдържанието на таблица
def show_table(table_name):
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    print(f"\n📋 Table: {table_name} ({len(rows)} rows)")
    for row in rows:
        print(row)

# 5️⃣ Извеждане на всички таблици
for table in reversed(tables):  # обръщаме за по-логичен ред
    show_table(table)

# 6️⃣ Затваряне на връзката
conn.close()
print("\n🔹 Database connection closed.")
