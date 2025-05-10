from rich.text import Text
from rich.table import Table
from readchar import key
from ..base import BasePrompt, Emoji


class ConfirmPrompt(BasePrompt):
    def __init__(self, message: str, default: bool = True, **kwargs):
        self.emoji = Emoji("question_mark")
        super().__init__(message, **kwargs)
        self.default = default

    def render(self) -> Table:
        table = Table.grid(padding=(0, 1))
        table.show_edge = False
        table.pad_edge = False

        table.add_row(self.message, Text("[Y/n]", style="bold green"))
        return table

    def handle_key(self, k: str) -> None:
        if k.lower() == "y":
            self.result = True
            self.done = True
        elif k.lower() == "n":
            self.result = False
            self.done = True
        elif k == key.ENTER:
            self.result = self.default
            self.done = True
        elif k == key.ESC:
            self.result = None
            self.done = True
