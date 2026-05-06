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


def test_select_prompt_normalizes_tuple_choices():
    prompt = SelectPrompt("Pick one:", [("Python", "py")])
    prompt.handle_key(key.ENTER)

    assert prompt.result == "py"


def test_select_prompt_cancel():
    prompt = SelectPrompt("Pick one:", ["apple"])
    prompt.handle_key(key.ESC)

    assert prompt.result is None
    assert prompt.done is True
