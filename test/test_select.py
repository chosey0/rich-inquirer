import pytest
from src import SelectPrompt
from src.base import Choice


def test_select_prompt(monkeypatch):
    keys = iter(["\r"])  # 바로 Enter
    monkeypatch.setattr("readchar.readkey", lambda: next(keys))

    choices = [Choice("apple"), Choice("banana"), Choice("grape")]
    prompt = SelectPrompt("Pick one:", choices)
    result = prompt.ask()

    assert result == "apple"
