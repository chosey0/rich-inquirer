# rich-inquirer

Interactive CLI prompts using [Rich](https://github.com/Textualize/rich) and readchar, inspired by python-inquirer.

## Features

- Text input with password masking
- Select and fuzzy select prompts
- Confirmation prompts
- Prompt chaining with `PromptContext`
- `Esc` cancellation returning `None`

## Install

```bash
pip install rich-inquirer
```

## Usage

```python
from rich_inquirer.prompt import TextPrompt, SelectPrompt, ConfirmPrompt, FuzzyPrompt

name = TextPrompt("What's your name?").ask()
language = SelectPrompt("Choose a language:", ["Python", "Go", "Rust"]).ask()
confirmed = ConfirmPrompt("Continue?", default=True).ask()
match = FuzzyPrompt("Search language:", ["Python", "TypeScript", "Rust"]).ask()
```

The prompt classes are also available from the top-level package:

```python
from rich_inquirer import TextPrompt
```

Use `Choice` when the displayed label should differ from the returned value.

```python
from rich_inquirer.base import Choice
from rich_inquirer.prompt import SelectPrompt

choice = SelectPrompt(
    "Choose a language:",
    [
        Choice("py", name="Python"),
        Choice("rs", name="Rust"),
    ],
).ask()
```

## PromptContext

```python
from rich_inquirer.context import PromptContext
from rich_inquirer.prompt import TextPrompt, SelectPrompt, ConfirmPrompt

context = PromptContext()
context.add("name", TextPrompt("Enter your name:"))
context.add("language", SelectPrompt("Choose language:", ["Python", "Go", "Rust"]))
context.add("confirm", ConfirmPrompt("Continue?", default=True))

results = context.run()
print(results)
```

If a prompt is cancelled with `Esc`, `PromptContext.run()` stops and returns the results collected so far.

## Development

```bash
pip install -e ".[dev]"
pytest
```
