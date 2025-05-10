import time
import threading
from readchar import readkey
from typing import List, Union
from abc import ABC, abstractmethod

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.emoji import Emoji

from .choice import Choice


class BasePrompt(ABC):
    emoji: Emoji

    def __init__(self, message: str, console: Console = None):
        self.message = Text(f"{self.emoji} {message}", style="bold black")
        self.console = console or Console()
        self.result = None
        self.done = False

    @abstractmethod
    def render(self) -> Table:
        """렌더링 결과를 반환하는 Table 구성"""
        ...

    @abstractmethod
    def handle_key(self, key: str) -> None:
        """입력된 키에 따라 내부 상태를 업데이트"""
        ...

    def _key_loop(self):
        while not self.done:
            k = readkey()
            self.handle_key(k)

    def ask(self):
        thread = threading.Thread(target=self._key_loop, daemon=True)
        thread.start()

        with Live(
            self.render(), console=self.console, refresh_per_second=30, transient=True
        ) as live:
            while not self.done:
                live.update(self.render())
                time.sleep(0.01)

        thread.join()

        try:
            self.console.print(self.message, Text(self.result, style="bold green"))
        except Exception as e:
            self.console.print(self.message, Text(f"{self.result}", style="bold green"))

        return self.result

    def _normalize_choices(
        self, choices: Union[List[str], List[Choice], List[tuple]]
    ) -> List[Choice]:
        _choices = []

        for choice in choices:
            if isinstance(choice, tuple):
                if len(choice) == 2:
                    name, value = choice
                else:
                    raise ValueError("Tuple must be of length 2")
            elif isinstance(choice, str):
                name = choice
                value = choice
            elif isinstance(choice, Choice):
                _choices.append(choice)
                continue
            else:
                raise TypeError("Choice must be str or tuple")

            _choices.append(Choice(value, name))

        return _choices
