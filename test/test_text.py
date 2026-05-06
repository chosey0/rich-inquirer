from readchar import key

from rich_inquirer.prompt import TextPrompt


def test_text_prompt_input_basic():
    prompt = TextPrompt("Enter your name:")
    prompt.handle_key("H")
    prompt.handle_key("i")
    prompt.handle_key(key.ENTER)
    assert prompt.result == "Hi"
    assert prompt.done is True


def test_text_prompt_backspace():
    prompt = TextPrompt("Enter:", password=False)
    for ch in "Test":
        prompt.handle_key(ch)
    prompt.handle_key(key.BACKSPACE)
    prompt.handle_key(key.ENTER)
    assert prompt.result == "Tes"


def test_password_prompt_formats_result_as_mask():
    prompt = TextPrompt("Password:", password=True)
    for ch in "secret":
        prompt.handle_key(ch)
    prompt.handle_key(key.ENTER)

    assert prompt.result == "secret"
    assert prompt._format_result() == "******"


def test_text_prompt_cancel():
    prompt = TextPrompt("Enter:")
    prompt.handle_key(key.ESC)

    assert prompt.result is None
    assert prompt.done is True


def test_text_prompt_uses_injected_read_key():
    keys = iter(["O", "K", key.ENTER])
    prompt = TextPrompt("Enter:", read_key=lambda: next(keys))

    assert prompt.ask() == "OK"


def test_text_prompt_ask_cancels_with_injected_escape():
    prompt = TextPrompt("Enter:", read_key=lambda: key.ESC)

    assert prompt.ask() is None
    assert prompt.done is True
