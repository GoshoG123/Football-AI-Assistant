from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static, RichLog
from textual.containers import Container, Vertical
from textual.reactive import reactive
from textual import events


from chatbot import handle_message




class FootballAssistant(App):
    CSS = """
    Screen {
        background: #0b0f1a;
        color: #e0e6ff;
    }


    #main {
        layout: vertical;
    }


    #output {
        height: 1fr;
        border: solid #1f2a44;
        padding: 1;
        background: #0f1629;
    }


    #input {
        dock: bottom;
        border: solid #1f2a44;
        background: #0f1629;
    }


    Header {
        background: #111a33;
        color: #7aa2ff;
    }


    Footer {
        background: #111a33;
        color: #7aa2ff;
    }
    """


    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            RichLog(id="output", highlight=True, markup=True),
            Input(placeholder="Въведи команда...", id="input"),
            id="main"
        )
        yield Footer()


    def on_mount(self):
        self.query_one("#output", RichLog).write("[bold cyan]⚽ Football Manager[/bold cyan]")
        self.query_one("#output", RichLog).write("Напиши 'помощ' за команди\n")


    def on_input_submitted(self, event: Input.Submitted):
        user_input = event.value.strip()
        output = self.query_one("#output", RichLog)


        if not user_input:
            return


        # показваме командата
        output.write(f"[bold green]> {user_input}[/bold green]")


        try:
            response = handle_message(user_input)
            output.write(f"[white]{response}[/white]")
        except Exception as e:
            output.write(f"[bold red]Грешка: {str(e)}[/bold red]")


        event.input.value = ""




if __name__ == "__main__":
    app = FootballAssistant()
    app.run()
