from db import get_connection
from services.players_service import get_all_players
from services.clubs_service import get_all_clubs
import datetime


# =========================
# HELPERS
# =========================
def find_player_by_name(name):
    players = get_all_players()
    for p in players:
        if p["full_name"].lower() == name.lower():
            return p
    return None


def find_club_by_name(name):
    clubs = get_all_clubs()
    for c in clubs:
        if c["name"].lower() == name.lower():
            return c
    return None


def is_valid_date(date_text):
    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# =========================
# TRANSFER PLAYER
# =========================
def transfer_player(player_name, from_club, to_club, date, fee=None):
    """
    Прави трансфер на играч с всички проверки и транзакция
    """

    # ========= ВАЛИДАЦИИ =========
    player = find_player_by_name(player_name)
    if not player:
        return False, f"Играчът '{player_name}' не съществува."

    to_club_obj = find_club_by_name(to_club)
    if not to_club_obj:
        return False, f"Клубът '{to_club}' не съществува."

    from_club_obj = None
    if from_club.lower() not in ("няма", "free", "none"):
        from_club_obj = find_club_by_name(from_club)
        if not from_club_obj:
            return False, f"Клубът '{from_club}' не съществува."

    # from != to
    if from_club_obj and from_club_obj["id"] == to_club_obj["id"]:
        return False, "Не може трансфер към същия клуб."

    # дата
    if not is_valid_date(date):
        return False, "Невалидна дата. Формат: YYYY-MM-DD."

    # fee
    if fee is not None:
        try:
            fee = float(fee)
            if fee < 0:
                return False, "Сумата трябва да е >= 0."
        except:
            return False, "Невалидна сума."

    # ========= БИЗНЕС ЛОГИКА =========
    current_club_id = player["club_id"]

    if current_club_id is None:
        if from_club_obj is not None:
            return False, "Играчът е свободен агент (няма клуб)."
    else:
        if not from_club_obj or current_club_id != from_club_obj["id"]:
            return False, "Играчът не е в този клуб."

    # ========= ТРАНЗАКЦИЯ =========
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # INSERT transfer
        cursor.execute("""
            INSERT INTO transfers (player_id, from_club_id, to_club_id, transfer_date, fee, note)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            player["id"],
            from_club_obj["id"] if from_club_obj else None,
            to_club_obj["id"],
            date,
            fee,
            None
        ))

        # UPDATE player club
        cursor.execute("""
            UPDATE players SET club_id = ?
            WHERE id = ?
        """, (to_club_obj["id"], player["id"]))

        # COMMIT само ако всичко е минало
        conn.commit()

        return True, f"Трансфер: {player_name} от {from_club} → {to_club} ({date})"

    except Exception as e:
        if conn:
            conn.rollback()  # 🔥 ВАЖНО за атомичност
        print("Transfer error:", e)
        return False, "Грешка при трансфера."

    finally:
        if conn:
            conn.close()


# =========================
# LIST TRANSFERS BY PLAYER
# =========================
def list_transfers_by_player(player_name):
    player = find_player_by_name(player_name)
    if not player:
        return []  # 🔥 важно: връщаме празен list

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.*, c1.name as from_club, c2.name as to_club
        FROM transfers t
        LEFT JOIN clubs c1 ON t.from_club_id = c1.id
        LEFT JOIN clubs c2 ON t.to_club_id = c2.id
        WHERE t.player_id = ?
        ORDER BY t.transfer_date DESC
    """, (player["id"],))

    transfers = cursor.fetchall()
    conn.close()

    return [dict(row) for row in transfers]


# =========================
# LIST TRANSFERS BY CLUB
# =========================
def list_transfers_by_club(club_name):
    club = find_club_by_name(club_name)
    if not club:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.*, p.full_name as player_name,
               COALESCE(c1.name, 'Свободен') as from_club,
               c2.name as to_club
        FROM transfers t
        JOIN players p ON t.player_id = p.id
        LEFT JOIN clubs c1 ON t.from_club_id = c1.id
        LEFT JOIN clubs c2 ON t.to_club_id = c2.id
        WHERE t.from_club_id = ? OR t.to_club_id = ?
        ORDER BY t.transfer_date DESC
    """, (club["id"], club["id"]))

    transfers = cursor.fetchall()
    conn.close()

    return [dict(row) for row in transfers]