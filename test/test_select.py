import pytest
from readchar import key

from rich_inquirer.prompt import SelectPrompt
from rich_inquirer.base import Choice


def test_select_prompt():
    choices = [Choice("apple"), Choice("banana"), Choice("grape")]
    prompt = SelectPrompt("Pick one:", choices)
    prompt.handle_key(key.ENTER)

    assert prompt.result == "apple"
    assert prompt.done is True


def test_select_prompt_moves_down():
    choices = [Choice("apple"), Choice("banana"), Choice("grape")]
    prompt = SelectPrompt("Pick one:", choices)
    prompt.handle_key(key.DOWN)
    prompt.handle_key(key.ENTER)

    assert prompt.result == "banana"


def test_select_prompt_requires_choices():
    with pytest.raises(ValueError):
        SelectPrompt("Pick one:", [])
