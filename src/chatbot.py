import json
import re
import os
from services.clubs_service import add_club, get_all_clubs, delete_club
from services.players_service import add_player, get_all_players, update_player, delete_player
from services.transfers_service import transfer_player, list_transfers_by_player, list_transfers_by_club
from utils.logger import log_command  # Logger за запис на всички команди

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
                response = ""

                # =====================
                # HELP
                # =====================
                if tag == "help":
                    response = (
                        "Команди:\n"
                        "- Добави клуб Име\n"
                        "- Покажи всички клубове\n"
                        "- Изтрий клуб Име\n"
                        "- Добави играч Име в Клуб позиция Позиция номер N\n"
                        "- Покажи играчи на Клуб\n"
                        "- Смени име/позиция/номер/статус на Име на Стойност\n"
                        "- Изтрий играч Име\n"
                        "- Трансфер Име от Клуб1 в Клуб2 YYYY-MM-DD [сума N]\n"
                        "- Покажи трансфери на Име\n"
                        "- Покажи трансфери на клуб Клуб\n"
                        "- Изход\n"
                    )

                # =====================
                # EXIT
                # =====================
                elif tag == "exit":
                    response = "Довиждане!\n"

                # =====================
                # ADD CLUB
                # =====================
                elif tag == "add_club":
                    club_name = match.group(1)
                    start_idx = original_message.lower().find(club_name.lower())
                    if start_idx != -1:
                        club_name = original_message[start_idx:start_idx + len(club_name)]
                    success = add_club(club_name, "Unknown", 0)
                    response = f"Клуб '{club_name}' е добавен.\n" if success else "Грешка или клубът вече съществува.\n"

                # =====================
                # LIST CLUBS
                # =====================
                elif tag == "list_clubs":
                    clubs = get_all_clubs()
                    if not clubs:
                        response = "Няма добавени клубове.\n"
                    else:
                        response = "Списък с клубове:\n"
                        for club in clubs:
                            response += f"- {club['name']}\n"

                # =====================
                # DELETE CLUB
                # =====================
                elif tag == "delete_club":
                    club_name = match.group(1)
                    start_idx = original_message.lower().find(club_name.lower())
                    if start_idx != -1:
                        club_name = original_message[start_idx:start_idx + len(club_name)]
                    success = delete_club(club_name)
                    response = f"Клуб '{club_name}' е изтрит.\n" if success else "Клубът не съществува.\n"

                # =====================
                # ADD PLAYER
                # =====================
                elif tag == "add_player":
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
                        response = f"Клубът '{club_name}' не съществува.\n"
                    else:
                        success = add_player(full_name, "2000-01-01", "Unknown", position, number, club_id)
                        response = f"Играч '{full_name}' е добавен в '{club_name}' като {position} с номер {number}.\n" if success else "Грешка при добавяне на играча.\n"

                # =====================
                # LIST PLAYERS
                # =====================
                elif tag == "list_players":
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
                        response = f"Клубът '{club_name}' не съществува.\n"
                    else:
                        players = get_all_players(club_id)
                        if not players:
                            response = f"Няма играчи в '{club_name}'.\n"
                        else:
                            response = f"Играчите на '{club_name}':\n"
                            for p in players:
                                response += f"- {p['full_name']} | {p['position']} | #{p['number']} | {p['status']}\n"

                # =====================
                # UPDATE PLAYER
                # =====================
                elif tag == "update_player":
                    field = match.group(1)
                    full_name = match.group(2)
                    new_value = match.group(3)
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
                        response = f"Играчът '{full_name}' не е намерен.\n"
                    else:
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
                            response = "Невалидно поле за редакция.\n"
                            success = False
                        if success:
                            response = f"Играчът '{full_name}' е обновен успешно.\n"
                        else:
                            response = "Грешка при обновяване.\n"

                # =====================
                # TRANSFER PLAYER
                # =====================
                elif tag == "transfer_player":
                    player_name = match.group(1)
                    from_club = match.group(2)
                    to_club = match.group(3)
                    date = match.group(4)
                    fee = None
                    if len(match.groups()) == 5:
                        fee = float(match.group(5))

                    def restore(text):
                        idx = original_message.lower().find(text.lower())
                        return original_message[idx:idx + len(text)] if idx != -1 else text

                    player_name = restore(player_name)
                    from_club = restore(from_club)
                    to_club = restore(to_club)

                    success, msg = transfer_player(player_name, from_club, to_club, date, fee)
                    response = msg + "\n"

                # =====================
                # SHOW TRANSFERS BY PLAYER
                # =====================
                elif tag == "show_transfers_player":
                    player_name = match.group(1)
                    idx = original_message.lower().find(player_name.lower())
                    if idx != -1:
                        player_name = original_message[idx:idx + len(player_name)]
                    transfers = list_transfers_by_player(player_name)
                    if not transfers:
                        response = f"Няма трансфери за '{player_name}'.\n"
                    else:
                        response = f"Трансфери на '{player_name}':\n"
                        for t in transfers:
                            fee_value = t['fee'] if t['fee'] is not None else "N/A"
                            response += f"- {t['transfer_date']} | {t['from_club']} → {t['to_club']} | {fee_value}\n"

                # =====================
                # SHOW TRANSFERS BY CLUB
                # =====================
                elif tag == "show_transfers_club":
                    club_name = match.group(1)
                    idx = original_message.lower().find(club_name.lower())
                    if idx != -1:
                        club_name = original_message[idx:idx + len(club_name)]

                    transfers = list_transfers_by_club(club_name)

                    if not transfers:
                        return f"Няма трансфери за клуб '{club_name}'.\n"

                    response = f"Трансфери на клуб '{club_name}':\n"
                    for t in transfers:
                        fee_value = t['fee'] if t['fee'] is not None else "N/A"
                        response += f"- {t['transfer_date']} | {t['player_name']} | {t['from_club']} → {t['to_club']} | {fee_value}\n"


                # =====================
                # DELETE PLAYER
                # =====================
                elif tag == "delete_player":
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
                        response = f"Играчът '{full_name}' не е намерен.\n"
                    else:
                        success = delete_player(player_id)
                        response = f"Играчът '{full_name}' е изтрит.\n" if success else "Грешка при изтриването на играча.\n"

                # =====================
                # НЕ РАЗБИРАМ КОМАНДАТА
                # =====================
                else:
                    response = "Не разбирам командата. Напиши 'помощ'.\n"

                # =====================
                # LOG COMMAND
                # =====================
                params = {}
                if tag in ["add_club", "delete_club", "list_players", "add_player", "update_player",
                           "transfer_player", "show_transfers_player", "show_transfers_club", "delete_player"]:
                    for i, g in enumerate(match.groups(), 1):
                        params[f"param{i}"] = g
                log_command(original_message, tag, params, response.strip())

                return response

    return "Не разбирам командата. Напиши 'помощ'.\n"