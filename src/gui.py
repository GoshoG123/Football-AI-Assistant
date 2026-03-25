import tkinter as tk
from tkinter import scrolledtext
from chatbot import handle_message

# =========================
# COLORS (Dark Blue Theme)
# =========================
BG_COLOR = "#0f172a"       # тъмно синьо
TEXT_COLOR = "#e2e8f0"     # светло
INPUT_BG = "#1e293b"
ACCENT = "#22d3ee"         # циан

FONT = ("Segoe UI", 11)
BOLD_FONT = ("Segoe UI", 11, "bold")  # <-- добавено

# =========================
# GUI APP
# =========================
class FootballApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Football AI Assistant")
        self.root.geometry("700x600")
        self.root.configure(bg=BG_COLOR)

        # CHAT DISPLAY
        self.chat_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            bg=INPUT_BG,
            fg=TEXT_COLOR,
            font=FONT,
            insertbackground=TEXT_COLOR,
            borderwidth=0
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)

        # 👉 TAG за bold текст
        self.chat_area.tag_config("bold", font=BOLD_FONT)

        # INPUT FRAME
        input_frame = tk.Frame(root, bg=BG_COLOR)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # ENTRY
        self.entry = tk.Entry(
            input_frame,
            bg=INPUT_BG,
            fg=TEXT_COLOR,
            font=FONT,
            insertbackground=TEXT_COLOR,
            borderwidth=0
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.send_message)

        # BUTTON
        send_btn = tk.Button(
            input_frame,
            text="Изпрати",
            bg=ACCENT,
            fg="black",
            font=("Segoe UI", 10, "bold"),
            command=self.send_message,
            borderwidth=0,
            padx=15,
            pady=5
        )
        send_btn.pack(side=tk.RIGHT)

        self.write_bot("Добре дошъл! Напиши 'помощ'.")

    # =========================
    # WRITE FUNCTIONS
    # =========================
    def write_user(self, message):
        self._write_message("👤: ", message)

    def write_bot(self, message):
        self._write_message("🤖: ", message)
        # Ако ботът казва "довиждане", затваряме програмата
        if "довиждане" in message.lower():
            self.root.after(800, self.root.destroy)  # малко забавяне за да се види съобщението

    def _write_message(self, prefix, message):
        self.chat_area.config(state=tk.NORMAL)

        # emoji НЕ bold
        self.chat_area.insert(tk.END, prefix)

        # текста bold
        self.chat_area.insert(tk.END, f"{message}\n\n", "bold")

        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    # =========================
    # SEND MESSAGE
    # =========================
    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        self.write_user(user_input)

        try:
            response = handle_message(user_input)
        except Exception as e:
            response = f"Грешка: {e}"

        self.write_bot(response)

        self.entry.delete(0, tk.END)


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = FootballApp(root)
    root.mainloop() 
