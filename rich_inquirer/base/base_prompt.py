import os
import sys
import time
import threading
from readchar import key as readchar_key, readkey
from readchar._config import config
from typing import Callable, List, Optional, Union
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


BRACKETED_PASTE_START = "\x1b[200~"
BRACKETED_PASTE_END = "\x1b[201~"


def _read_key(escape_timeout: float = 0.1) -> str:
    """Read one key, treating a lone ESC as a complete keypress."""
    if select is None or termios is None:
        return readkey()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    term = termios.tcgetattr(fd)

    def read_byte(timeout: Optional[float] = None) -> Union[bytes, None]:
        if timeout is not None:
            readable, _, _ = select.select([sys.stdin], [], [], timeout)
            if not readable:
                return None
        return os.read(fd, 1)

    def read_char(timeout: Optional[float] = None) -> Union[str, None]:
        first = read_byte(timeout=timeout)
        if first is None:
            return None

        data = first
        while True:
            try:
                return data.decode()
            except UnicodeDecodeError as exc:
                if exc.reason != "unexpected end of data":
                    raise
                next_byte = read_byte(timeout=escape_timeout)
                if next_byte is None:
                    raise
                data += next_byte

    def read_next(timeout: float = escape_timeout) -> Union[str, None]:
        readable, _, _ = select.select([sys.stdin], [], [], timeout)
        if not readable:
            return None
        return read_char()

    def read_escape_sequence() -> str:
        sequence = readchar_key.ESC
        introducer = read_next()
        if introducer is None:
            return sequence

        sequence += introducer
        if introducer not in "\x4f\x5b":
            return sequence

        while True:
            char = read_next()
            if char is None:
                return sequence
            sequence += char
            if "\x40" <= char <= "\x7e":
                return sequence

    def read_available_text(first: str) -> str:
        text = first
        while True:
            char = read_next(timeout=0)
            if char is None:
                return text
            text += char

    def read_bracketed_paste() -> str:
        text = ""
        while not text.endswith(BRACKETED_PASTE_END):
            text += read_char()
        return text[: -len(BRACKETED_PASTE_END)]

    try:
        term[3] &= ~(termios.ICANON | termios.ECHO | termios.IGNBRK | termios.BRKINT)
        termios.tcsetattr(fd, termios.TCSAFLUSH, term)

        c1 = read_char()
        if c1 in config.INTERRUPT_KEYS:
            raise KeyboardInterrupt
        if c1 != readchar_key.ESC:
            return read_available_text(c1)

        sequence = read_escape_sequence()
        if sequence == BRACKETED_PASTE_START:
            return read_bracketed_paste()
        return sequence
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
