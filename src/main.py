from chatbot import handle_message
import datetime
import os

# =========================
# Път за логване на команди
# =========================
BASE_DIR = os.path.dirname(__file__)
LOG_FILE = os.path.join(BASE_DIR, "commands.log")


def log_command(command_text, response_text):
    """Записва timestamp, въведен текст и резултат в лог файл"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Command: {command_text}\n")
        f.write(f"[{timestamp}] Response: {response_text}\n\n")


def main():
    print("Добре дошли в Football AI Assistant Chatbot!")
    print("Напишете 'помощ' за списък с команди или 'изход' за приключване.\n")

    while True:
        user_input = input(">>> ").strip()
        if not user_input:
            continue  # пропуска празен input

        response = handle_message(user_input)
        print(response)

        # Логваме командата и отговора
        log_command(user_input, response)

        # Прекратяваме цикъла при exit
        if response.lower() in ("довиждане!", "exit", "quit", "изход"):
            break


if __name__ == "__main__":
    main()
