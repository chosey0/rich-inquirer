import pytest
from readchar import key

from rich_inquirer.prompt import FuzzyPrompt
from rich_inquirer.base import Choice


def test_fuzzy_prompt():
    choices = [
        Choice("apple"),
        Choice("banana"),
        Choice("blueberry"),
        Choice("blackberry"),
    ]

    prompt = FuzzyPrompt("Choose:", choices)
    prompt.handle_key("b")
    prompt.handle_key("l")
    prompt.handle_key(key.ENTER)

    assert prompt.result in ["blueberry", "blackberry"]
    assert prompt.done is True


def test_fuzzy_prompt_requires_choices():
    with pytest.raises(ValueError):
        FuzzyPrompt("Choose:", [])


def test_fuzzy_prompt_requires_positive_limit():
    with pytest.raises(ValueError):
        FuzzyPrompt("Choose:", ["apple"], limit=0)
