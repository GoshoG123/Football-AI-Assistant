from services.standings_service import get_standings


# =========================
# SHOW STANDINGS
# =========================
def handle_show_standings(match):

    league = match.group(1)
    season = match.group(2)

    success, msg = get_standings(
        league,
        season
    )

    return msg