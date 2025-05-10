import os
import sys

sys.path.append(os.path.realpath("."))

from src.context import PromptContext
from src.base.choice import Choice

context = PromptContext()

context.add("username", TextPrompt("Enter your name:"))
context.add("language", SelectPrompt("Select language:", ["Python", "Rust", "Go"]))
context.add("confirm", ConfirmPrompt("Do you want to continue?", default=True))

results = context.run()

print("\n[Prompt Summary]")
for key, value in results.items():
    print(f"{key}: {value}")