from db import get_connection




# =========================
# CREATE LEAGUE
# =========================
def create_league(name, season):
    conn = get_connection()
    cursor = conn.cursor()


    try:
        cursor.execute("""
            INSERT INTO leagues (name, season)
            VALUES (?, ?)
        """, (name, season))


        conn.commit()
        return cursor.lastrowid


    except Exception as e:
        print("Create league error:", e)
        return None


    finally:
        conn.close()




# =========================
# GET LEAGUE
# =========================
def get_league(name, season):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT * FROM leagues
        WHERE name = ? AND season = ?
    """, (name, season))


    league = cursor.fetchone()
    conn.close()


    return dict(league) if league else None




# =========================
# ADD TEAM TO LEAGUE
# =========================
def add_team_to_league(league_id, club_id):
    conn = get_connection()
    cursor = conn.cursor()


    try:
        cursor.execute("""
            INSERT INTO league_teams (league_id, club_id)
            VALUES (?, ?)
        """, (league_id, club_id))


        conn.commit()
        return True


    except Exception as e:
        print("Add team error:", e)
        return False


    finally:
        conn.close()




# =========================
# REMOVE TEAM FROM LEAGUE
# =========================
def remove_team_from_league(league_id, club_id):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        DELETE FROM league_teams
        WHERE league_id = ? AND club_id = ?
    """, (league_id, club_id))


    conn.commit()
    success = cursor.rowcount > 0


    conn.close()
    return success




# =========================
# GET TEAMS IN LEAGUE
# =========================
def get_league_teams(league_id):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT c.*
        FROM league_teams lt
        JOIN clubs c ON lt.club_id = c.id
        WHERE lt.league_id = ?
    """, (league_id,))


    teams = cursor.fetchall()
    conn.close()


    return [dict(row) for row in teams]




# =========================
# CHECK IF TEAM EXISTS IN LEAGUE
# =========================
def team_exists_in_league(league_id, club_id):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT 1 FROM league_teams
        WHERE league_id = ? AND club_id = ?
    """, (league_id, club_id))


    exists = cursor.fetchone() is not None
    conn.close()


    return exists




# =========================
# CLEAR MATCHES (for regenerate)
# =========================
def clear_matches(league_id):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        DELETE FROM matches
        WHERE league_id = ?
    """, (league_id,))


    conn.commit()
    conn.close()




# =========================
# INSERT MATCH
# =========================
def insert_match(league_id, round_no, home_id, away_id):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO matches (league_id, round_no, home_club_id, away_club_id)
        VALUES (?, ?, ?, ?)
    """, (league_id, round_no, home_id, away_id))


    conn.commit()
    conn.close()




# =========================
# GET MATCHES BY LEAGUE
# =========================
def get_matches_by_league(league_id):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT m.*, c1.name as home_team, c2.name as away_team
        FROM matches m
        JOIN clubs c1 ON m.home_club_id = c1.id
        JOIN clubs c2 ON m.away_club_id = c2.id
        WHERE m.league_id = ?
        ORDER BY m.round_no ASC
    """, (league_id,))


    matches = cursor.fetchall()
    conn.close()


    return [dict(row) for row in matches]

