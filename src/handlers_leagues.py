from services.leagues_service import (
    create_league,
    add_team_to_league,
    list_league_teams,
    remove_team_from_league,
    generate_schedule,
    get_schedule
)



# =========================
# CREATE LEAGUE
# =========================
def handle_create_league(match):
    name = match.group(1)
    season = match.group(2)


    success, msg = create_league(name, season)
    return msg




# =========================
# ADD TEAM
# =========================
def handle_add_team(match):
    club_name = match.group(1)
    league_name = match.group(2)
    season = match.group(3)


    success, msg = add_team_to_league(club_name, league_name, season)
    return msg




# =========================
# LIST TEAMS
# =========================
def handle_list_teams(match):
    league_name = match.group(1)
    season = match.group(2)


    success, msg = list_league_teams(league_name, season)
    return msg




# =========================
# REMOVE TEAM
# =========================
def handle_remove_team(match):
    club_name = match.group(1)
    league_name = match.group(2)
    season = match.group(3)


    success, msg = remove_team_from_league(club_name, league_name, season)
    return msg




# =========================
# GENERATE SCHEDULE
# =========================
def handle_generate_schedule(match):
    league_name = match.group(1)
    season = match.group(2)


    success, msg = generate_schedule(league_name, season)
    return msg




# =========================
# SHOW SCHEDULE
# =========================
def handle_show_schedule(match):
    league_name = match.group(1)
    season = match.group(2)

    matches = get_schedule(league_name, season)

    if not matches:
        return f"Няма програма за '{league_name}' ({season})."

    response = f"Програма за '{league_name}' ({season}):\n"

    current_round = None
    for m in matches:
        if current_round != m["round_no"]:
            current_round = m["round_no"]
            response += f"\nКръг {current_round}:\n"

        response += f"- {m['home_team']} vs {m['away_team']}\n"

    return response