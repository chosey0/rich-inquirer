from rich_inquirer.prompt import TextPrompt

prompt = TextPrompt("Enter your password:", password=True)
result = prompt.ask()
prompt.console.log(result)
