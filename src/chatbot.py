import json
import re
import os
from clubs_service import add_club, get_all_clubs, delete_club

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
                        "- Покажи всички\n"
                        "- Изтрий клуб Име\n"
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
                    if success:
                        return f"Клуб '{club_name}' е добавен.\n"
                    else:
                        return "Грешка или клубът вече съществува.\n"

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
                    # Вземаме оригиналното име от съобщението
                    club_name = match.group(1)
                    start_idx = original_message.lower().find(club_name.lower())
                    if start_idx != -1:
                        club_name = original_message[start_idx:start_idx + len(club_name)]

                    success = delete_club(club_name)
                    if success:
                        return f"Клуб '{club_name}' е изтрит.\n"
                    else:
                        return "Клубът не съществува.\n"

    return "Не разбирам командата. Напиши 'помощ'.\n"
