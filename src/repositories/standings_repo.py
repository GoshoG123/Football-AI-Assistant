from db import get_connection


# =========================
# GET LEAGUE TEAMS
# =========================
def get_league_teams(league_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.id, c.name
        FROM league_teams lt
        JOIN clubs c ON lt.club_id = c.id
        WHERE lt.league_id = ?
    """, (league_id,))

    teams = cursor.fetchall()

    conn.close()

    return [dict(row) for row in teams]


# =========================
# GET PLAYED MATCHES
# =========================
def get_played_matches(league_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM matches
        WHERE league_id = ?
        AND status = 'played'
    """, (league_id,))

    matches = cursor.fetchall()

    conn.close()

    return [dict(row) for row in matches]