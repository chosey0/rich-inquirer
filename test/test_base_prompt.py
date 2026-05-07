import os
import sys
import threading
import time

from readchar import key

from rich_inquirer.base.base_prompt import (
    BRACKETED_PASTE_END,
    BRACKETED_PASTE_START,
    _read_key,
)


def _read_from_pty(monkeypatch, value: str, escape_timeout: float = 0.1) -> str:
    master_fd, slave_fd = os.openpty()
    stdin = os.fdopen(slave_fd, "r")

    def write_value():
        time.sleep(0.01)
        os.write(master_fd, value.encode())

    writer = threading.Thread(target=write_value)
    try:
        monkeypatch.setattr(sys, "stdin", stdin)
        writer.start()
        return _read_key(escape_timeout=escape_timeout)
    finally:
        writer.join(timeout=1)
        stdin.close()
        os.close(master_fd)


def test_read_key_returns_lone_escape(monkeypatch):
    assert _read_from_pty(monkeypatch, key.ESC, escape_timeout=0.01) == key.ESC


def test_read_key_preserves_escape_sequences(monkeypatch):
    assert _read_from_pty(monkeypatch, key.DOWN) == key.DOWN


def test_read_key_returns_available_pasted_text(monkeypatch):
    assert _read_from_pty(monkeypatch, "pasted text") == "pasted text"


def test_read_key_returns_multibyte_text(monkeypatch):
    assert _read_from_pty(monkeypatch, "한글") == "한글"


def test_read_key_extracts_bracketed_paste(monkeypatch):
    value = f"{BRACKETED_PASTE_START}pasted text{BRACKETED_PASTE_END}"

    assert _read_from_pty(monkeypatch, value) == "pasted text"


def test_read_key_extracts_multibyte_bracketed_paste(monkeypatch):
    value = f"{BRACKETED_PASTE_START}한글 붙여넣기{BRACKETED_PASTE_END}"

    assert _read_from_pty(monkeypatch, value) == "한글 붙여넣기"
