from rich.text import Text
from rich.table import Table
from readchar import key
from rapidfuzz import fuzz

from typing import List, Union
from ..base import BasePrompt, Emoji, Choice


class FuzzyPrompt(BasePrompt):
    def __init__(
        self,
        message: str,
        choices: Union[List[str], List[Choice]],
        limit: int = 5,
        **kwargs,
    ):
        self.emoji = Emoji("magnifying_glass_tilted_right")
        super().__init__(message, **kwargs)
        self.all_choices: List[Choice] = self._normalize_choices(choices)
        self.filtered_choices: List[Choice] = self.all_choices[:limit]
        self.input_buffer = ""
        self.cursor_index = 0
        self.limit = limit

    def render(self) -> Table:
        table = Table.grid(padding=(0, 1))
        table.add_row(
            self.message,
            Text(self.input_buffer, style="bold black"),
        )

        for i, choice in enumerate(self.filtered_choices):
            line = Text(choice.name)
            if i == self.cursor_index:
                line.stylize("bold green")
            else:
                line.stylize("dim")
            table.add_row(line)
        return table

    def _fuzzy_filter(self):
        query = self.input_buffer.lower()
        if not query:
            self.filtered_choices = self.all_choices[: self.limit]
            self.cursor_index = 0
            return

        scored = [
            (choice, fuzz.ratio(query, choice.name.lower()))
            for choice in self.all_choices
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        self.filtered_choices = [c for c, _ in scored[: self.limit]]
        self.cursor_index = 0  # reset to top match

    def handle_key(self, k: str) -> None:
        if k == key.ENTER:
            if self.filtered_choices:
                self.result = self.filtered_choices[self.cursor_index].value
            else:
                self.result = None
            self.done = True
        elif k == key.BACKSPACE:
            self.input_buffer = self.input_buffer[:-1]
            self._fuzzy_filter()
        elif k == key.UP:
            self.cursor_index = (self.cursor_index - 1) % len(self.filtered_choices)
        elif k == key.DOWN:
            self.cursor_index = (self.cursor_index + 1) % len(self.filtered_choices)
        elif k == key.ESC:
            self.result = None
            self.done = True
        elif len(k) == 1 and k.isprintable():
            self.input_buffer += k
            self._fuzzy_filter()
