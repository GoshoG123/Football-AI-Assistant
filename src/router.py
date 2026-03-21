from services.clubs_service import add_club, get_all_clubs, delete_club
from services.players_service import add_player, get_all_players, update_player, delete_player
from services.transfers_service import transfer_player, list_transfers_by_player, list_transfers_by_club


def route_intent(tag, params):
    """
    Router: получава tag и параметри от NLU и връща готов отговор.
    """
    if tag == "add_club":
        club_name = params.get("club_name")
        success = add_club(club_name, "Unknown", 0)
        return f"Клуб '{club_name}' е добавен.\n" if success else "Грешка или клубът вече съществува.\n"

    if tag == "list_clubs":
        clubs = get_all_clubs()
        if not clubs:
            return "Няма добавени клубове.\n"
        response = "Списък с клубове:\n"
        for c in clubs:
            response += f"- {c['name']}\n"
        return response + "\n"

    if tag == "delete_club":
        club_name = params.get("club_name")
        success = delete_club(club_name)
        return f"Клуб '{club_name}' е изтрит.\n" if success else "Клубът не съществува.\n"

    if tag == "add_player":
        full_name = params.get("full_name")
        club_name = params.get("club_name")
        position = params.get("position").upper()
        number = int(params.get("number"))

        clubs = get_all_clubs()
        club_id = None
        for c in clubs:
            if c['name'].lower() == club_name.lower():
                club_id = c['id']
                break

        if not club_id:
            return f"Клубът '{club_name}' не съществува.\n"

        success = add_player(full_name, "2000-01-01", "Unknown", position, number, club_id)
        return f"Играч '{full_name}' е добавен в '{club_name}' като {position} с номер {number}.\n" if success else "Грешка при добавяне на играча.\n"

    if tag == "list_players":
        club_name = params.get("club_name")
        clubs = get_all_clubs()
        club_id = None
        for c in clubs:
            if c['name'].lower() == club_name.lower():
                club_id = c['id']
                break

        if not club_id:
            return f"Клубът '{club_name}' не съществува.\n"

        players = get_all_players(club_id)
        if not players:
            return f"Няма играчи в '{club_name}'.\n"

        response = f"Играчите на '{club_name}':\n"
        for p in players:
            response += f"- {p['full_name']} | {p['position']} | #{p['number']} | {p['status']}\n"
        return response + "\n"

    if tag == "update_player":
        player_id = None
        full_name = params.get("full_name")
        new_value = params.get("new_value")
        field = params.get("field").lower()

        players = get_all_players()
        for p in players:
            if p['full_name'].lower() == full_name.lower():
                player_id = p['id']
                break

        if not player_id:
            return f"Играчът '{full_name}' не е намерен.\n"

        if field == "име":
            success = update_player(player_id, full_name=new_value)
        elif field == "позиция":
            success = update_player(player_id, position=new_value.upper())
        elif field == "номер":
            success = update_player(player_id, number=int(new_value))
        elif field == "статус":
            success = update_player(player_id, status=new_value.capitalize())
        else:
            return "Невалидно поле за редакция.\n"

        return f"Играчът '{full_name}' е обновен успешно.\n" if success else "Грешка при обновяване.\n"

    if tag == "delete_player":
        full_name = params.get("full_name")
        player_id = None
        players = get_all_players()
        for p in players:
            if p['full_name'].lower() == full_name.lower():
                player_id = p['id']
                break
        if not player_id:
            return f"Играчът '{full_name}' не е намерен.\n"

        success = delete_player(player_id)
        return f"Играчът '{full_name}' е изтрит.\n" if success else "Грешка при изтриването на играча.\n"

    if tag == "transfer_player":
        player_name = params.get("player_name")
        from_club = params.get("from_club")
        to_club = params.get("to_club")
        date = params.get("date")
        fee = params.get("fee")

        success, msg = transfer_player(player_name, from_club, to_club, date, fee)
        return msg + "\n"

    if tag == "show_transfers_player":
        player_name = params.get("player_name")
        transfers = list_transfers_by_player(player_name)
        if not transfers:
            return f"Няма трансфери за '{player_name}'.\n"

        response = f"Трансфери на '{player_name}':\n"
        for t in transfers:
            fee_value = t['fee'] if t['fee'] is not None else "—"
            response += f"- {t['transfer_date']} | {t['from_club']} → {t['to_club']} | {fee_value}\n"
        return response + "\n"

    if tag == "show_transfers_club":
        club_name = params.get("club_name")
        transfers = list_transfers_by_club(club_name)
        if not transfers:
            return f"Няма трансфери за клуб '{club_name}'.\n"

        response = f"Трансфери на клуб '{club_name}':\n"
        for t in transfers:
            fee_value = t['fee'] if t['fee'] is not None else "—"
            response += f"- {t['transfer_date']} | {t['player_name']} | {t['from_club']} → {t['to_club']} | {fee_value}\n"
        return response + "\n"

    return "Не разбирам командата.\n"