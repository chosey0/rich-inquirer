from rich.text import Text
from rich.table import Table
from readchar import key
from typing import Union, List

from ..base import BasePrompt, Emoji, Choice


class SelectPrompt(BasePrompt):
    def __init__(
        self,
        message: str,
        choices: Union[List[str], List[Choice], List[tuple]],
        **kwargs,
    ):
        self.emoji = Emoji("question_mark")
        super().__init__(message, **kwargs)
        self.choices: List[Choice] = self._normalize_choices(choices)
        self.selected_index = 0

    def render(self) -> Table:
        table = Table.grid(padding=(0, 1))
        table.expand = True
        table.title_justify = "left"

        table.title = self.message
        table.show_edge = False
        table.pad_edge = False

        for i, choice in enumerate(self.choices):
            prefix = Emoji("arrow_forward") if i == self.selected_index else "  "
            line = Text(f"{prefix} {choice.name}")
            if i == self.selected_index:
                line.stylize("bold green")
            table.add_row(line)

        return table

    def handle_key(self, k: str) -> None:
        if k == key.UP:
            self.selected_index = (self.selected_index - 1) % len(self.choices)
        elif k == key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.choices)
        elif k == key.ENTER:
            self.result = self.choices[self.selected_index].value
            self.done = True
        elif k == key.ESC:
            self.result = None
            self.done = True
