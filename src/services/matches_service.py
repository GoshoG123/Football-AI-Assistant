from repositories.matches_repo import (
    get_matches_by_round,
    update_match_result,
    insert_goal,
    insert_card,
    get_match_events,
    get_match_by_id
)
from db import get_connection


from repositories.leagues_repo import get_league
from services.clubs_service import get_all_clubs
from services.players_service import get_all_players




# текущ мач (runtime)
CURRENT_MATCH_ID = None




# =========================
# SET CURRENT MATCH
# =========================
def set_current_match(match_id):
    global CURRENT_MATCH_ID
    CURRENT_MATCH_ID = match_id
    return True, f"Избран мач #{match_id}"




# =========================
# SHOW ROUND
# =========================
def show_round(league_name, season, round_no):
    league = get_league(league_name, season)
    if not league:
        return False, "Няма такава лига."


    matches = get_matches_by_round(league["id"], round_no)


    if not matches:
        return False, "Няма мачове за този кръг."


    response = f"Кръг {round_no}:\n"
    for m in matches:
        score = (
            f"{m['home_goals']}:{m['away_goals']}"
            if m["status"] == "played"
            else "vs"
        )
        response += f"#{m['id']} {m['home_team']} {score} {m['away_team']}\n"


    return True, response



# =========================
# SAVE RESULT
# =========================
def save_result(match_id, home_goals, away_goals):
    if CURRENT_MATCH_ID is None:
        return False, "Няма избран мач."

    if home_goals < 0 or away_goals < 0:
        return False, "Невалиден резултат."

    update_match_result(
        CURRENT_MATCH_ID,
        home_goals,
        away_goals
    )

    return True, (
        f"Резултатът е записан "
        f"({home_goals}:{away_goals})"
    )



# =========================
# ADD GOAL
# =========================
def add_goal(player_name, club_name, minute):
    if CURRENT_MATCH_ID is None:
        return False, "Няма избран мач."

    if minute < 1 or minute > 120:
        return False, "Невалидна минута."

    players = get_all_players()
    clubs = get_all_clubs()

    player = next(
        (p for p in players if p["full_name"].strip().lower() == player_name.strip().lower()),
        None
    )
    if not player:
        return False, "Няма такъв играч."

    club = next(
        (c for c in clubs if c["name"].strip().lower() == club_name.strip().lower()),
        None
    )
    if not club:
        return False, "Няма такъв отбор."

    from repositories.matches_repo import get_matches_by_round
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM matches WHERE id = ?", (CURRENT_MATCH_ID,))
    match = cursor.fetchone()
    conn.close()

    if not match:
        return False, "Мачът не съществува."

    if club["id"] not in [match["home_club_id"], match["away_club_id"]]:
        return False, "Отборът не участва в този мач."

    if player["club_id"] != club["id"]:
        return False, "Играчът не е от този отбор."

    insert_goal(CURRENT_MATCH_ID, player["id"], club["id"], minute)

    return True, f"Гол на {player_name} ({minute} мин.)"




# =========================
# ADD CARD
# =========================
def add_card(player_name, club_name, card_type, minute):
    if CURRENT_MATCH_ID is None:
        return False, "Няма избран мач."

    if minute < 1 or minute > 120:
        return False, "Невалидна минута."

    card_type = card_type.upper()

    if card_type not in ['Y', 'R']:
        return False, "Невалиден тип картон."

    players = get_all_players()
    clubs = get_all_clubs()

    player = next(
        (p for p in players if p["full_name"].strip().lower() == player_name.strip().lower()),
        None
    )
    if not player:
        return False, "Няма такъв играч."

    club = next(
        (c for c in clubs if c["name"].strip().lower() == club_name.strip().lower()),
        None
    )
    if not club:
        return False, "Няма такъв отбор."

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM matches WHERE id = ?", (CURRENT_MATCH_ID,))
    match = cursor.fetchone()
    conn.close()

    if not match:
        return False, "Мачът не съществува."

    if club["id"] not in [match["home_club_id"], match["away_club_id"]]:
        return False, "Отборът не участва в този мач."

    if player["club_id"] != club["id"]:
        return False, "Играчът не е от този отбор."

    insert_card(CURRENT_MATCH_ID, player["id"], club["id"], minute, card_type)

    return True, f"Картон ({card_type}) за {player_name}"




# =========================
# SHOW EVENTS
# =========================
def show_events():
    if CURRENT_MATCH_ID is None:
        return False, "Няма избран мач."

    events = get_match_events(CURRENT_MATCH_ID)

    response = "Събития:\n"

    # EVENTS
    if events:
        for e in events:

            if e["type"] == "goal":
                response += (
                    f"{e['minute']}' ⚽ "
                    f"{e['player_name']} "
                    f"({e['club_name']})\n"
                )

            elif e["type"] == "Y":
                response += (
                    f"{e['minute']}' 🟨 "
                    f"{e['player_name']} "
                    f"({e['club_name']})\n"
                )

            elif e["type"] == "R":
                response += (
                    f"{e['minute']}' 🟥 "
                    f"{e['player_name']} "
                    f"({e['club_name']})\n"
                )

    # RESULT
    match = get_match_by_id(CURRENT_MATCH_ID)

    if match:
        response += "\n--------------------------------------------\n\n"

        if match["status"] == "played":
            response += (
                f"Резултат:\n"
                f"{match['home_team']} "
                f"{match['home_goals']}:{match['away_goals']} "
                f"{match['away_team']}\n"
            )
        else:
            response += "Мачът още няма резултат.\n"

    return True, response
