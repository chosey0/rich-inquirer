from rich.text import Text
from rich.table import Table
from readchar import key
from ..base import BasePrompt, Emoji


class TextPrompt(BasePrompt):
    def __init__(self, message: str, password: bool = False, **kwargs):
        self.emoji = Emoji("pen")
        super().__init__(message, **kwargs)
        self.password = password
        self.buffer = ""

    def render(self) -> Table:
        table = Table.grid(padding=(0, 1))
        table.show_edge = False
        table.pad_edge = False
        table.add_row(
            self.message,
            Text(
                ("*" * len(self.buffer) if self.password else self.buffer),
                style="bold white",
            ),
        )
        return table

    def handle_key(self, k: str) -> None:
        if k == key.ENTER:
            self.result = self.buffer
            self.done = True
        elif k == key.BACKSPACE:
            self.buffer = self.buffer[:-1]
        elif k == key.ESC:
            self.result = None
            self.done = True
        elif len(k) == 1 and k.isprintable():
            self.buffer += k
