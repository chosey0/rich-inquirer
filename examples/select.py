from rich_inquirer.prompt import SelectPrompt


prompt = SelectPrompt(
    "Choose your favorite programming language:",
    ["Python", "Rust", "Go", "JavaScript"],
)
result = prompt.ask()
prompt.console.log(result)
