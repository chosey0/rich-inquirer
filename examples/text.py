from rich_inquirer.prompt import TextPrompt


prompt = TextPrompt("Enter your text:")
result = prompt.ask()
prompt.console.log(result)
