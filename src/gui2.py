import tkinter as tk
from tkinter import ttk, scrolledtext

from chatbot import handle_message
from services.clubs_service import get_all_clubs


class FootballDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Football Manager Dashboard")
        self.root.geometry("1300x750")
        self.root.configure(bg="#0b0f1a")

        # =========================
        # STYLE
        # =========================
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="#0f1629",
                        foreground="#e0e6ff",
                        fieldbackground="#0f1629",
                        rowheight=35,
                        font=("Arial", 12, "bold"))

        style.configure("Treeview.Heading",
                        background="#16213e",
                        foreground="#7aa2ff",
                        font=("Arial", 13, "bold"))

        style.map("Treeview",
                  background=[("selected", "#1f2a4d")],
                  foreground=[("selected", "#ffffff")])
    

        # =========================
        # MAIN PANELS
        # =========================
        self.left = tk.Frame(root, bg="#0f1629", width=320)
        self.left.pack(side=tk.LEFT, fill=tk.Y)
        self.left.pack_propagate(False)

        self.center = tk.Frame(root, bg="#0b0f1a", width=530)
        self.center.pack(side=tk.LEFT, fill=tk.Y)
        self.center.pack_propagate(False)

        self.right = tk.Frame(root, bg="#0f1629", width= 480)
        self.right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # =========================
        # LEFT PANEL (NAVIGATION)
        # =========================
        tk.Label(
            self.left,
            text="📊 МЕНЮ",
            bg="#0f1629",
            fg="#7aa2ff",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        self.menu = ttk.Treeview(self.left)
        self.menu.pack(fill=tk.BOTH, expand=True, padx=10)
        self.menu.tag_configure("club", font=("Arial", 11, "bold"))

        # MAIN ITEMS
        self.clubs_item = self.menu.insert("", "end", text="🏆 Отбори")
        self.players_item = self.menu.insert("", "end", text="👤 Играчите")
        self.matches_item = self.menu.insert("", "end", text="⚽ Мачове")
        self.rounds_item = self.menu.insert("", "end", text="📅 Кръгове")
        self.events_item = self.menu.insert("", "end", text="📌 Събития")

        # зареждаме клубове под "Играчите"
        self.load_clubs_dropdown()

        self.menu.bind("<<TreeviewSelect>>", self.left_click)

        # =========================
        # CENTER PANEL (HELP)
        # =========================
        tk.Label(
            self.center,
            text="📌 КОМАНДИ",
            bg="#0b0f1a",
            fg="#7aa2ff",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        self.help_box = scrolledtext.ScrolledText(
            self.center,
            bg="#0f1629",
            fg="#e0e6ff",
            font=("Consolas", 12),
            height=25
        )
        self.help_box.pack(fill=tk.BOTH, expand=True)

        self.help_box.insert(tk.END,
            "⚽ КОМАНДИ:\n\n"
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
                        "- Създай лига Име Сезон\n"
                        "- Добави отбор Клуб в лига Име Сезон\n"
                        "- Покажи отбори в лига Име Сезон\n"
                        "- Премахни отбор Клуб от лига Име Сезон\n"
                        "- Генерирай програма Име Сезон\n"
                        "- Покажи програма Име Сезон\n"
                        "- Покажи кръг N Лига Сезон\n"
                        "- Избери мач ID\n"
                        "- Резултат Отбор1-Отбор2 X:Y запиши\n"
                        "- Гол Играч Отбор Минута минута\n"
                        "- Картон Играч Отбор Y/R Минута\n"
                        "- Покажи събития\n"
                        "- Изход\n"
        )

        self.help_box.configure(state="disabled")

        # =========================
        # INPUT FIELD
        # =========================
        self.input = tk.Entry(
            self.center,
            bg="#16213e",
            fg="white",
            font=("Arial", 12)
        )
        self.input.pack(fill=tk.X)
        self.input.bind("<Return>", self.send_command)

        # =========================
        # RIGHT PANEL
        # =========================
        tk.Label(
            self.right,
            text="🔎 РЕЗУЛТАТ",
            bg="#0f1629",
            fg="#7aa2ff",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        self.detail_box = scrolledtext.ScrolledText(
            self.right,
            bg="#0b0f1a",
            fg="#7aa2ff",
            font=("Consolas", 12)
        )
        self.detail_box.pack(fill=tk.BOTH, expand=True)

    # =========================
    # LOAD CLUBS DROPDOWN
    # =========================
    def load_clubs_dropdown(self):
        clubs = get_all_clubs()

        for c in clubs:
            self.menu.insert(self.players_item, "end", text=c["name"], tags=("club",))

    # =========================
    # COMMAND INPUT
    # =========================
    def send_command(self, event=None):
        text = self.input.get().strip()
        if not text:
            return

        try:
            response = handle_message(text)

            self.detail_box.delete("1.0", tk.END)
            self.detail_box.insert(tk.END, response)

        except Exception as e:
            self.detail_box.delete("1.0", tk.END)
            self.detail_box.insert(tk.END, f"Error: {e}")

        self.input.delete(0, tk.END)

    # =========================
    # LEFT NAV CLICK
    # =========================
    def left_click(self, event):
        selected_item = self.menu.focus()
        text = self.menu.item(selected_item, "text")

        # ако е клуб вътре в "Играчите"
        parent = self.menu.parent(selected_item)

        if parent == self.players_item:
            cmd = f"покажи играчи на {text}"
            response = handle_message(cmd)

        elif text == "🏆 Отбори":
            response = handle_message("покажи всички клубове")

        elif text == "⚽ Мачове":
            response = handle_message("покажи кръг 1 Тест 2020/2021")

        elif text == "📅 Кръгове":
            response = handle_message("покажи програма Тест 2020/2021")

        elif text == "📌 Събития":
            response = handle_message("покажи събития")

        else:
            return

        self.detail_box.delete("1.0", tk.END)
        self.detail_box.insert(tk.END, response)


if __name__ == "__main__":
    root = tk.Tk()
    app = FootballDashboard(root)
    root.mainloop()
