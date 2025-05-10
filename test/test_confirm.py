import pytest
from rich_inquirer.prompt import ConfirmPrompt


def test_confirm_prompt_true(monkeypatch):
    keys = iter(["y"])
    monkeypatch.setattr("readchar.readkey", lambda: next(keys))

    prompt = ConfirmPrompt("Proceed?")
    result = prompt.ask()

    assert result is True


def test_confirm_prompt_false(monkeypatch):
    keys = iter(["n"])
    monkeypatch.setattr("readchar.readkey", lambda: next(keys))

    prompt = ConfirmPrompt("Proceed?")
    result = prompt.ask()

    assert result is False
