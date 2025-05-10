import os
import sys

sys.path.append(os.path.realpath("."))

from src import TextPrompt

prompt = TextPrompt("Enter your text:")
result = prompt.ask()
prompt.console.log(result)
