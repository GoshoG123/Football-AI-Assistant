from services.matches_service import (
    set_current_match,
    show_round,
    save_result,
    add_goal,
    add_card,
    show_events
)




def handle_select_match(match):
    match_id = int(match.group(1))
    success, msg = set_current_match(match_id)
    return msg




def handle_show_round(match):
    round_no = int(match.group(1))
    league = match.group(2)
    season = match.group(3)


    success, msg = show_round(league, season, round_no)
    return msg




def handle_result(match):

    team1 = match.group(1)
    team2 = match.group(2)

    goals1 = int(match.group(3))
    goals2 = int(match.group(4))

    success, msg = save_result(
        team1,
        team2,
        goals1,
        goals2
    )

    return msg


def handle_goal(match):
    original = match.string.lower()

    from services.players_service import get_all_players
    from services.clubs_service import get_all_clubs

    players = get_all_players()
    clubs = get_all_clubs()

    player = None
    for p in players:
        if p["full_name"].lower() in original:
            player = p
            break

    if not player:
        return "Няма такъв играч."

    club = None
    for c in clubs:
        if c["name"].lower() in original:
            club = c
            break

    if not club:
        return "Няма такъв отбор."

    minute = int(match.group(3))

    success, msg = add_goal(player["full_name"], club["name"], minute)
    return msg



def handle_card(match):
    original = match.string.lower()

    from services.players_service import get_all_players
    from services.clubs_service import get_all_clubs

    players = get_all_players()
    clubs = get_all_clubs()

    player = None
    for p in players:
        if p["full_name"].lower() in original:
            player = p
            break

    if not player:
        return "Няма такъв играч."

    club = None
    for c in clubs:
        if c["name"].lower() in original:
            club = c
            break

    if not club:
        return "Няма такъв отбор."

    card = match.group(3).upper()
    minute = int(match.group(4))

    success, msg = add_card(player["full_name"], club["name"], card, minute)
    return msg

def handle_show_events(match):
    success, msg = show_events()
    return msg
