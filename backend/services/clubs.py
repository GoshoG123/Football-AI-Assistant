from db import get_connection


# =========================
# CREATE
# =========================
def add_club(name, city, founded_year):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO clubs (name, city, founded_year) VALUES (?, ?, ?)",
            (name, city, founded_year)
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
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clubs")
    clubs = cursor.fetchall()

    conn.close()
    return clubs


# =========================
# READ - BY NAME
# =========================
def get_club_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM clubs WHERE name = ?",
        (name,)
    )

    club = cursor.fetchone()
    conn.close()
    return club


# =========================
# UPDATE
# =========================
def update_club(name, new_city, new_year):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE clubs SET city = ?, founded_year = ? WHERE name = ?",
            (new_city, new_year, name)
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
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM clubs WHERE name = ?",
            (name,)
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
