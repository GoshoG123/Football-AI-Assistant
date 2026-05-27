from repositories.leagues_repo import get_league
from repositories.standings_repo import (
    get_league_teams,
    get_played_matches
)


# =========================
# GET STANDINGS
# =========================
def get_standings(league_name, season):

    league = get_league(league_name, season)

    if not league:
        return False, "Няма такава лига."

    teams = get_league_teams(league["id"])

    if not teams:
        return False, "Няма отбори в тази лига."

    matches = get_played_matches(league["id"])

    if not matches:
        response = "Няма изиграни мачове.\n\n"

        pos = 1

        for team in standings.values():

            response += (
                "{pos}. "
                "{team['team']} | "
                f"0 MP | 0 W | 0 D | 0 L | "
                f"0:0 | GD 0 | 0 pts\n"
            )

            pos += 1

        return True, response

    standings = {}

    # =========================
    # INIT TABLE
    # =========================
    for team in teams:

        standings[team["id"]] = {
            "team": team["name"],
            "MP": 0,
            "W": 0,
            "D": 0,
            "L": 0,
            "GF": 0,
            "GA": 0,
            "GD": 0,
            "PTS": 0
        }

    # =========================
    # CALCULATE
    # =========================
    for match in matches:

        home_id = match["home_club_id"]
        away_id = match["away_club_id"]

        home_goals = match["home_goals"]
        away_goals = match["away_goals"]

        # MP
        standings[home_id]["MP"] += 1
        standings[away_id]["MP"] += 1

        # GOALS
        standings[home_id]["GF"] += home_goals
        standings[home_id]["GA"] += away_goals

        standings[away_id]["GF"] += away_goals
        standings[away_id]["GA"] += home_goals

        # RESULT
        if home_goals > away_goals:

            standings[home_id]["W"] += 1
            standings[home_id]["PTS"] += 3

            standings[away_id]["L"] += 1

        elif away_goals > home_goals:

            standings[away_id]["W"] += 1
            standings[away_id]["PTS"] += 3

            standings[home_id]["L"] += 1

        else:

            standings[home_id]["D"] += 1
            standings[away_id]["D"] += 1

            standings[home_id]["PTS"] += 1
            standings[away_id]["PTS"] += 1

    # =========================
    # GD
    # =========================
    for team in standings.values():
        team["GD"] = team["GF"] - team["GA"]

    # =========================
    # SORT
    # =========================
    table = sorted(
        standings.values(),
        key=lambda t: (
            -t["PTS"],
            -t["GD"],
            -t["GF"],
            t["team"]
        )
    )

    # =========================
    # FORMAT
    # =========================
    response = (
        f"КЛАСИРАНЕ\n\n"
    )

    pos = 1

    for t in table:

        response += (
            f"{pos}. "
            f"{t['team']} | "
            f"{t['MP']} MP | "
            f"{t['W']} W | "
            f"{t['D']} D | "
            f"{t['L']} L | "
            f"{t['GF']}:{t['GA']} | "
            f"GD {t['GD']} | "
            f"{t['PTS']} pts\n"
        )

        pos += 1

    return True, response