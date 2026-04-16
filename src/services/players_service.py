from db import get_connection
from datetime import datetime

VALID_POSITIONS = {"GK", "DF", "MF", "FW"}

# =========================
# CREATE
# =========================
def add_player(full_name, birth_date, nationality, position, number, club_id):
    """
    Добавя нов играч
    Валидации:
    - position ∈ {'GK','DF','MF','FW'}
    - number ∈ 1-99
    - birth_date валидна дата 'YYYY-MM-DD'
    """
    # Валидация
    if position not in VALID_POSITIONS:
        print("Невалидна позиция. Изберете GK, DF, MF или FW.")
        return False

    if not (1 <= number <= 99):
        print("Невалиден номер. Трябва да е между 1 и 99.")
        return False

    try:
        datetime.strptime(birth_date, "%Y-%m-%d")
    except ValueError:
        print("Невалидна дата. Формат: YYYY-MM-DD")
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Проверка за duplicate (същото име + клуб)
        cursor.execute(
            "SELECT * FROM players WHERE full_name = ? AND club_id = ?",
            (full_name, club_id)
        )
        if cursor.fetchone():
            print("Играчът вече съществува в този клуб.")
            return False

        cursor.execute(
            """INSERT INTO players
            (full_name, birth_date, nationality, position, number, status, club_id)
            VALUES (?, ?, ?, ?, ?, 'active', ?)""",
            (full_name, birth_date, nationality, position, number, club_id)
        )

        conn.commit()
        return True

    except Exception as e:
        print("Error adding player:", e)
        return False

    finally:
        conn.close()


# =========================
# READ
# =========================
def get_all_players(club_id=None):
    conn = get_connection()
    cursor = conn.cursor()


    if club_id:
        cursor.execute("SELECT * FROM players WHERE club_id = ?", (club_id,))
    else:
        cursor.execute("SELECT * FROM players")


    players = cursor.fetchall()
    conn.close()


    return [dict(p) for p in players]


# =========================
# UPDATE
# =========================
def update_player(player_id, full_name=None, position=None, number=None, status=None):
    """
    Редакция на играч
    Може да се промени име, позиция, номер или статус
    """

    if position is not None and position not in VALID_POSITIONS:
        print("Невалидна позиция. Изберете GK, DF, MF или FW.")
        return False

    if number is not None and not (1 <= number <= 99):
        print("Невалиден номер. Трябва да е между 1 и 99.")
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Създаваме динамично SET statement
        updates = []
        values = []

        if full_name is not None:
            updates.append("full_name = ?")
            values.append(full_name)

        if position is not None:
            updates.append("position = ?")
            values.append(position)

        if number is not None:
            updates.append("number = ?")
            values.append(number)

        if status is not None:
            updates.append("status = ?")
            values.append(status)

        if not updates:
            print("Няма подадени полета за update.")
            return False

        values.append(player_id)
        sql = f"UPDATE players SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(sql, tuple(values))
        conn.commit()

        if cursor.rowcount == 0:
            return False  # няма такъв играч

        return True

    except Exception as e:
        print("Error updating player:", e)
        return False

    finally:
        conn.close()


# =========================
# DELETE
# =========================
def delete_player(player_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM players WHERE id = ?", (player_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return False  # няма такъв играч
        return True

    except Exception as e:
        print("Error deleting player:", e)
        return False

    finally:
        conn.close()
