from rich_inquirer.context import PromptContext
from rich_inquirer.prompt import TextPrompt, SelectPrompt, ConfirmPrompt

context = PromptContext()
context.add("name", TextPrompt("Enter your name:"))
context.add("lang", SelectPrompt("Choose language:", ["Python", "Go", "Rust"]))
context.add("confirm", ConfirmPrompt("Continue?", default=True))

results = context.run()
print(results)
