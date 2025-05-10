from rich_inquirer.prompt import TextPrompt


def test_text_prompt_input_basic():
    prompt = TextPrompt("Enter your name:")
    prompt.handle_key("H")
    prompt.handle_key("i")
    prompt.handle_key("\r")  # Enter key
    assert prompt.result == "Hi"
    assert prompt.done is True


def test_text_prompt_backspace():
    prompt = TextPrompt("Enter:", password=False)
    for ch in "Test":
        prompt.handle_key(ch)
    prompt.handle_key("\x7f")  # BACKSPACE
    prompt.handle_key("\r")  # Enter
    assert prompt.result == "Tes"
