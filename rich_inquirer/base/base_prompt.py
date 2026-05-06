import os
import sys
import time
import threading
from readchar import key as readchar_key, readkey
from readchar._config import config
from typing import Callable, List, Union
from abc import ABC, abstractmethod

try:
    import select
    import termios
except ImportError:
    select = None
    termios = None

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.emoji import Emoji

from .choice import Choice


def _read_key(escape_timeout: float = 0.1) -> str:
    """Read one key, treating a lone ESC as a complete keypress."""
    if select is None or termios is None:
        return readkey()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    term = termios.tcgetattr(fd)

    def read_next(timeout: float = escape_timeout) -> Union[str, None]:
        readable, _, _ = select.select([sys.stdin], [], [], timeout)
        if not readable:
            return None
        return os.read(fd, 1).decode()

    try:
        term[3] &= ~(termios.ICANON | termios.ECHO | termios.IGNBRK | termios.BRKINT)
        termios.tcsetattr(fd, termios.TCSAFLUSH, term)

        c1 = os.read(fd, 1).decode()
        if c1 in config.INTERRUPT_KEYS:
            raise KeyboardInterrupt
        if c1 != readchar_key.ESC:
            return c1

        c2 = read_next()
        if c2 is None:
            return c1
        if c2 not in "\x4F\x5B":
            return c1 + c2

        c3 = read_next()
        if c3 is None or c3 not in "\x31\x32\x33\x35\x36":
            return c1 + c2 + (c3 or "")

        c4 = read_next()
        if c4 is None or c4 not in "\x30\x31\x33\x34\x35\x37\x38\x39":
            return c1 + c2 + c3 + (c4 or "")

        c5 = read_next()
        return c1 + c2 + c3 + c4 + (c5 or "")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


class BasePrompt(ABC):
    emoji: Emoji

    def __init__(
        self,
        message: str,
        console: Console = None,
        read_key: Callable[[], str] = _read_key,
    ):
        self.message = Text(f"{self.emoji} {message}", style="bold black")
        self.console = console or Console()
        self.read_key = read_key
        self.result = None
        self.done = False

    @abstractmethod
    def render(self) -> Table:
        """렌더링 결과를 반환하는 Table 구성"""
        ...

    @abstractmethod
    def _handle_key(self, key: str) -> None:
        """입력된 키에 따라 프롬프트별 상태를 업데이트"""
        ...

    def handle_key(self, key: str) -> None:
        """Handle shared cancellation before prompt-specific key handling."""
        if key == readchar_key.ESC:
            self.result = None
            self.done = True
            return
        self._handle_key(key)

    def _key_loop(self):
        while not self.done:
            k = self.read_key()
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

        thread.join(timeout=0.1)

        self.console.print(self.message, Text(self._format_result(), style="bold green"))

        return self.result

    def _format_result(self) -> str:
        return "" if self.result is None else str(self.result)

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
