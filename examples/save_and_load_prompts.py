import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from promptex.promptex import Promptex
from promptex.elements import *
from promptex.encoding_strategy import *


promptex = Promptex()

promptex.set_elements(
    [
        Instruction("Create an innovative quest for a new fantasy RPG game."),
        OutputFormat("Markdown text in English"),
    ]
)

# Save path
path = "examples/test.json"

# Save the prompt to a file
promptex.save_prompt(path)

# Load the prompt from a file
promptex = promptex.load_prompt(path)

# Display the prompt result
strategy = SimpleTextEncodingStrategy()
prompt = strategy.encode(promptex)
print(prompt)
