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

        label = "[Y/n]" if self.default else "[y/N]"
        table.add_row(self.message, Text(label, style="bold green"))
        return table

    def _handle_key(self, k: str) -> None:
        if k.lower() == "y":
            self.result = True
            self.done = True
        elif k.lower() == "n":
            self.result = False
            self.done = True
        elif k == key.ENTER:
            self.result = self.default
            self.done = True
