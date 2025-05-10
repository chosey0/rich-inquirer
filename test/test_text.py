import pytest
from src import TextPrompt


def test_text_prompt(monkeypatch):
    keys = iter(["h", "e", "l", "l", "o", "\r"])
    monkeypatch.setattr("readchar.readkey", lambda: next(keys))

    prompt = TextPrompt("Your name?")
    result = prompt.ask()

    assert result == "hello"
