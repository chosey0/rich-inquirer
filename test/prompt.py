from src import (
    TextPrompt,
    SelectPrompt,
    ConfirmPrompt,
    FuzzyPrompt,
)
from src.base.choice import Choice
from rich.console import Console

# Example


def text_prompt():
    console = Console()
    prompt = TextPrompt("What's your name?")
    name = prompt.ask()


def password_prompt():
    console = Console()
    prompt = TextPrompt("Enter your password:", password=True)
    result = prompt.ask()


def select_prompt():
    console = Console()
    prompt = SelectPrompt(
        message="Choose your favorite programming language",
        choices=["Python", "Rust", "Go", "JavaScript"],
    )
    answer = prompt.ask()


def confirm_prompt():
    console = Console()
    prompt = ConfirmPrompt("Do you want to continue?", default=True)
    answer = prompt.ask()


def fuzzy_prompt():

    choices = [
        Choice("python", name="Python"),
        Choice("typescript", name="TypeScript"),
        Choice("go", name="Go"),
        Choice("rust", name="Rust"),
        Choice("ruby", name="Ruby"),
        Choice("java", name="Java"),
        Choice("kotlin", name="Kotlin"),
        Choice("swift", name="Swift"),
    ]

    console = Console()
    selected = FuzzyPrompt("Search language", choices, console=console).ask()
    console.print(f"You selected: [bold green]{selected}[/bold green]")
