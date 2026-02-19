from db import get_connection


# =========================
# CREATE
# =========================
def add_club(name, city, founded_year):
    # ✅ Валидация за празно име
    if not name or name.strip() == "":
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # ✅ Проверка за duplicate
        cursor.execute("SELECT id FROM clubs WHERE name = ?", (name,))
        if cursor.fetchone():
            return False  # клубът вече съществува

        cursor.execute(
            "INSERT INTO clubs (name, city, founded_year) VALUES (?, ?, ?)",
            (name.strip(), city, founded_year)
        )

        conn.commit()
        return True

    except Exception as e:
        print("Error adding club:", e)
        return False

    finally:
        conn.close()


# =========================
# READ - ALL
# =========================
def get_all_clubs():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM clubs")
        clubs = cursor.fetchall()

        return clubs

    except Exception as e:
        print("Error fetching clubs:", e)
        return []

    finally:
        conn.close()


# =========================
# READ - BY NAME
# =========================
def get_club_by_name(name):
    if not name or name.strip() == "":
        return None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM clubs WHERE name = ?",
            (name.strip(),)
        )

        club = cursor.fetchone()
        return club

    except Exception as e:
        print("Error fetching club:", e)
        return None

    finally:
        conn.close()


# =========================
# UPDATE
# =========================
def update_club(name, new_city, new_year):
    if not name or name.strip() == "":
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE clubs SET city = ?, founded_year = ? WHERE name = ?",
            (new_city, new_year, name.strip())
        )

        conn.commit()

        if cursor.rowcount == 0:
            return False  # няма такъв клуб

        return True

    except Exception as e:
        print("Error updating club:", e)
        return False

    finally:
        conn.close()


# =========================
# DELETE
# =========================
def delete_club(name):
    if not name or name.strip() == "":
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM clubs WHERE name = ?",
            (name.strip(),)
        )

        conn.commit()

        if cursor.rowcount == 0:
            return False  # няма такъв клуб

        return True

    except Exception as e:
        print("Error deleting club:", e)
        return False

    finally:
        conn.close()
