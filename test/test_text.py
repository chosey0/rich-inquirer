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
