import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "commands.log")


def log_command(raw_input, intent, params, result):
    """
    Записва командата в commands.log с timestamp, intent, params и резултат
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Параметрите като кратък речник
    params_str = ", ".join(f"{k}={v}" for k, v in params.items())
    
    log_entry = f"[{timestamp}] INPUT: {raw_input} | INTENT: {intent} | PARAMS: {params_str} | RESULT: {result}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)