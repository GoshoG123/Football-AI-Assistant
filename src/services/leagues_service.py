from repositories.leagues_repo import (
    create_league as repo_create_league,
    get_league,
    add_team_to_league as repo_add_team_to_league,
    remove_team_from_league as repo_remove_team_from_league,
    get_league_teams as repo_get_league_teams,
    team_exists_in_league,
    insert_match,
    clear_matches,
    get_matches_by_league
)


from services.clubs_service import get_all_clubs
import re


# =========================
# HELPERS
# =========================
def is_valid_season(season):
    """
    Проверка за формат YYYY/YYYY
    """
    return re.fullmatch(r"\d{4}/\d{4}", season) is not None




def find_club_by_name(name):
    clubs = get_all_clubs()
    for c in clubs:
        if c["name"].lower() == name.lower():
            return c
    return None




# =========================
# CREATE LEAGUE
# =========================
def create_league(name, season):
    if not is_valid_season(season):
        return False, "Невалиден сезон. Формат: YYYY/YYYY"


    existing = get_league(name, season)
    if existing:
        return False, "Лигата вече съществува."


    league_id = repo_create_league(name, season)
    if not league_id:
        return False, "Грешка при създаване на лига."


    return True, f"Създадена лига '{name}' ({season})"




# =========================
# ADD TEAM
# =========================
def add_team_to_league(club_name, league_name, season):
    league = get_league(league_name, season)
    if not league:
        return False, "Няма такава лига."


    club = find_club_by_name(club_name)
    if not club:
        return False, f"Клубът '{club_name}' не съществува."


    if team_exists_in_league(league["id"], club["id"]):
        return False, "Отборът вече е в тази лига."


    success = repo_add_team_to_league(league["id"], club["id"])
    return (
        (True, f"Добавен '{club_name}' в лига '{league_name}'.")
        if success else
        (False, "Грешка при добавяне.")
    )




# =========================
# REMOVE TEAM
# =========================
def remove_team_from_league(club_name, league_name, season):
    league = get_league(league_name, season)
    if not league:
        return False, "Няма такава лига."


    club = find_club_by_name(club_name)
    if not club:
        return False, "Клубът не съществува."


    success = repo_remove_team_from_league(league["id"], club["id"])
    return (
        (True, "Отборът е премахнат.")
        if success else
        (False, "Отборът не е в тази лига.")
    )




# =========================
# LIST TEAMS
# =========================
def list_league_teams(league_name, season):
    league = get_league(league_name, season)
    if not league:
        return False, "Няма такава лига."

    teams = repo_get_league_teams(league["id"])

    if not teams:
        return True, "Няма отбори в тази лига."

    response = f"Отбори в лига '{league_name}' ({season}):\n"
    for t in teams:
        response += f"- {t['name']}\n"

    return True, response




# =========================
# GENERATE ROUND ROBIN
# =========================
def generate_schedule(league_name, season):
    league = get_league(league_name, season)
    if not league:
        return False, "Няма такава лига."


    teams = repo_get_league_teams(league["id"])
    if len(teams) < 4:
        return False, "Недостатъчно отбори (минимум 4)."


    # Ако вече има мачове → не позволявай повторно генериране
    existing_matches = get_matches_by_league(league["id"])
    if existing_matches:
        return False, "Програмата вече съществува. Използвайте 'прегенерирай', за да изтриете старата."


    team_ids = [t["id"] for t in teams]
    team_names = {t["id"]: t["name"] for t in teams}


    # Ако нечетен брой → добавяме BYE
    if len(team_ids) % 2 != 0:
        team_ids.append(None)


    n = len(team_ids)
    rounds = n - 1
    half = n // 2


    schedule = []


    for r in range(rounds):
        round_matches = []


        for i in range(half):
            t1 = team_ids[i]
            t2 = team_ids[n - 1 - i]


            if t1 is None or t2 is None:
                continue


            insert_match(league["id"], r + 1, t1, t2)
            round_matches.append((t1, t2))


        # Ротация (circle method)
        team_ids = [team_ids[0]] + [team_ids[-1]] + team_ids[1:-1]


        schedule.append(round_matches)


    total_matches = sum(len(r) for r in schedule)


    response = f"Програмата е генерирана!\nКръгове: {rounds}\nМачове: {total_matches}\n\nПърви кръг:\n"
    for t1, t2 in schedule[0]:
        response += f"- {team_names[t1]} vs {team_names[t2]}\n"


    return True, response




# =========================
# GET MATCHES
# =========================
def get_schedule(league_name, season):
    league = get_league(league_name, season)
    if not league:
        return []


    matches = get_matches_by_league(league["id"])
    return matches

