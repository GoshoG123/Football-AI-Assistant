import json
import re
import os
from services.clubs_service import add_club, get_all_clubs, delete_club
from services.players_service import add_player, get_all_players, update_player, delete_player

# =========================
# Зареждане на intents.json
# =========================
BASE_DIR = os.path.dirname(__file__)
INTENTS_FILE = os.path.join(BASE_DIR, "intents.json")

with open(INTENTS_FILE, "r", encoding="utf-8") as f:
    intents = json.load(f)["intents"]

def handle_message(message):
    original_message = message.strip()
    message_lower = original_message.lower()

    for intent in intents:
        for pattern in intent["patterns"]:
            match = re.fullmatch(pattern, message_lower)
            if match:
                tag = intent["tag"]

                # =====================
                # HELP
                # =====================
                if tag == "help":
                    return (
                        "Команди:\n"
                        "- Добави клуб Име\n"
                        "- Покажи всички клубове\n"
                        "- Изтрий клуб Име\n"
                        "- Добави играч Име в Клуб позиция Позиция номер N\n"
                        "- Покажи играчи на Клуб\n"
                        "- Смени име/позиция/номер/статус на Име на Стойност\n"
                        "- Изтрий играч Име\n"
                        "- Изход\n"
                    )

                # =====================
                # EXIT
                # =====================
                if tag == "exit":
                    return "Довиждане!\n"

                # =====================
                # ADD CLUB
                # =====================
                if tag == "add_club":
                    club_name = match.group(1)

                    start_idx = original_message.lower().find(club_name.lower())
                    if start_idx != -1:
                        club_name = original_message[start_idx:start_idx + len(club_name)]

                    success = add_club(club_name, "Unknown", 0)
                    return f"Клуб '{club_name}' е добавен.\n" if success else "Грешка или клубът вече съществува.\n"

                # =====================
                # LIST CLUBS
                # =====================
                if tag == "list_clubs":
                    clubs = get_all_clubs()
                    if not clubs:
                        return "Няма добавени клубове.\n"

                    response = "Списък с клубове:\n"
                    for club in clubs:
                        response += f"- {club['name']}\n"
                    return response + "\n"

                # =====================
                # DELETE CLUB
                # =====================
                if tag == "delete_club":
                    club_name = match.group(1)

                    start_idx = original_message.lower().find(club_name.lower())
                    if start_idx != -1:
                        club_name = original_message[start_idx:start_idx + len(club_name)]

                    success = delete_club(club_name)
                    return f"Клуб '{club_name}' е изтрит.\n" if success else "Клубът не съществува.\n"

                # =====================
                # ADD PLAYER
                # =====================
                if tag == "add_player":
                    full_name = match.group(1)
                    club_name = match.group(2)

                    start_idx = original_message.lower().find(full_name.lower())
                    if start_idx != -1:
                        full_name = original_message[start_idx:start_idx + len(full_name)]

                    start_idx_club = original_message.lower().find(club_name.lower())
                    if start_idx_club != -1:
                        club_name = original_message[start_idx_club:start_idx_club + len(club_name)]

                    position = match.group(3).upper()
                    number = int(match.group(4))

                    clubs = get_all_clubs()
                    club_id = None
                    for c in clubs:
                        if c['name'].lower() == club_name.lower():
                            club_id = c['id']
                            break

                    if not club_id:
                        return f"Клубът '{club_name}' не съществува.\n"

                    success = add_player(full_name, "2000-01-01", "Unknown", position, number, club_id)
                    return (
                        f"Играч '{full_name}' е добавен в '{club_name}' като {position} с номер {number}.\n"
                        if success else "Грешка при добавяне на играча.\n"
                    )

                # =====================
                # LIST PLAYERS
                # =====================
                if tag == "list_players":
                    club_name = match.group(1)

                    start_idx = original_message.lower().find(club_name.lower())
                    if start_idx != -1:
                        club_name = original_message[start_idx:start_idx + len(club_name)]

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

                # =====================
                # UPDATE PLAYER (NAME / POSITION / NUMBER / STATUS)
                # =====================
                if tag == "update_player":
                    field = match.group(1)
                    full_name = match.group(2)
                    new_value = match.group(3)

                    # Възстановяваме оригиналното име
                    start_idx = original_message.lower().find(full_name.lower())
                    if start_idx != -1:
                        full_name = original_message[start_idx:start_idx + len(full_name)]

                    players = get_all_players()
                    player_id = None

                    for p in players:
                        if p['full_name'].lower() == full_name.lower():
                            player_id = p['id']
                            break

                    if not player_id:
                        return f"Играчът '{full_name}' не е намерен.\n"

                    field = field.lower()

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

                    if success:
                        return f"Играчът '{full_name}' е обновен успешно.\n"
                    else:
                        return "Грешка при обновяване.\n"

                # =====================
                # DELETE PLAYER
                # =====================
                if tag == "delete_player":
                    full_name = match.group(1)

                    start_idx = original_message.lower().find(full_name.lower())
                    if start_idx != -1:
                        full_name = original_message[start_idx:start_idx + len(full_name)]

                    players = get_all_players()
                    player_id = None

                    for p in players:
                        if p['full_name'].lower() == full_name.lower():
                            player_id = p['id']
                            break

                    if not player_id:
                        return f"Играчът '{full_name}' не е намерен.\n"

                    success = delete_player(player_id)
                    return (
                        f"Играчът '{full_name}' е изтрит.\n"
                        if success else "Грешка при изтриването на играча.\n"
                    )

    return "Не разбирам командата. Напиши 'помощ'.\n"