import os
import sys

sys.path.append(os.path.realpath("."))

from src.prompt import FuzzyPrompt
from src.base.choice import Choice


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

prompt = FuzzyPrompt("Search language", choices)
result = prompt.ask()
prompt.console.log(result)
