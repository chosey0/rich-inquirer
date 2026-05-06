from readchar import key

from rich_inquirer.prompt import ConfirmPrompt


def test_confirm_prompt_true():
    prompt = ConfirmPrompt("Proceed?")
    prompt.handle_key("y")

    assert prompt.result is True
    assert prompt.done is True


def test_confirm_prompt_false():
    prompt = ConfirmPrompt("Proceed?")
    prompt.handle_key("n")

    assert prompt.result is False
    assert prompt.done is True


def test_confirm_prompt_uses_default_on_enter():
    prompt = ConfirmPrompt("Proceed?", default=False)
    prompt.handle_key(key.ENTER)

    assert prompt.result is False
    assert prompt.done is True
