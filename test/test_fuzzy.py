import pytest
from src import FuzzyPrompt
from src.base import Choice


def test_fuzzy_prompt(monkeypatch):
    keys = iter(["b", "l", "\r"])  # filter to 'blackberry' or 'blueberry'
    monkeypatch.setattr("readchar.readkey", lambda: next(keys))

    choices = [
        Choice("apple"),
        Choice("banana"),
        Choice("blueberry"),
        Choice("blackberry"),
    ]

    prompt = FuzzyPrompt("Choose:", choices)
    result = prompt.ask()

    assert result in ["blueberry", "blackberry"]
