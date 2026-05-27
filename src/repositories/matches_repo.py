from db import get_connection




# =========================
# GET MATCHES BY ROUND
# =========================
def get_matches_by_round(league_id, round_no):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT m.*, c1.name as home_team, c2.name as away_team
        FROM matches m
        JOIN clubs c1 ON m.home_club_id = c1.id
        JOIN clubs c2 ON m.away_club_id = c2.id
        WHERE m.league_id = ? AND m.round_no = ?
    """, (league_id, round_no))


    matches = cursor.fetchall()
    conn.close()


    return [dict(row) for row in matches]




# =========================
# UPDATE RESULT
# =========================
def update_match_result(match_id, home_goals, away_goals):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE matches
        SET
            home_goals = ?,
            away_goals = ?,
            status = 'played'
        WHERE id = ?
    """, (home_goals, away_goals, match_id))

    conn.commit()
    conn.close()




# =========================
# ADD GOAL
# =========================
def insert_goal(match_id, player_id, club_id, minute):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO goals (match_id, player_id, club_id, minute)
        VALUES (?, ?, ?, ?)
    """, (match_id, player_id, club_id, minute))


    conn.commit()
    conn.close()




# =========================
# ADD CARD
# =========================
def insert_card(match_id, player_id, club_id, minute, card_type):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO cards (match_id, player_id, club_id, minute, card_type)
        VALUES (?, ?, ?, ?, ?)
    """, (match_id, player_id, club_id, minute, card_type))


    conn.commit()
    conn.close()



# =========================
# GET EVENTS
# =========================
def get_match_events(match_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            'goal' as type,
            g.minute,
            p.full_name as player_name,
            c.name as club_name,
            NULL as card_type

        FROM goals g
        JOIN players p ON g.player_id = p.id
        JOIN clubs c ON g.club_id = c.id

        WHERE g.match_id = ?

        UNION ALL

        SELECT
            ca.card_type as type,
            ca.minute,
            p.full_name as player_name,
            c.name as club_name,
            ca.card_type

        FROM cards ca
        JOIN players p ON ca.player_id = p.id
        JOIN clubs c ON ca.club_id = c.id

        WHERE ca.match_id = ?

        ORDER BY minute
    """, (match_id, match_id))

    events = cursor.fetchall()

    conn.close()

    return [dict(row) for row in events]




# =========================
# GET MATCH BY ID
# =========================
def get_match_by_id(match_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            m.*,
            c1.name as home_team,
            c2.name as away_team
        FROM matches m
        JOIN clubs c1 ON m.home_club_id = c1.id
        JOIN clubs c2 ON m.away_club_id = c2.id
        WHERE m.id = ?
    """, (match_id,))

    match = cursor.fetchone()

    conn.close()

    return dict(match) if match else None
