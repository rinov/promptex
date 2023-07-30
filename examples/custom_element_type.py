import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from promptex.promptex import Promptex
from promptex.elements import *
from promptex.encoding_strategy import *


# Add a new element type
class Example(Element):
    def __init__(self, text: str):
        super().__init__("example", text)


promptex = Promptex()

promptex.set_elements(
    [
        Instruction("Create an innovative quest for a new fantasy RPG game."),
        OutputFormat("Markdown text in English").add_element(
            Example("# Quest: The Lost Sword of the Kingdom")
        ),
    ]
)

strategy = SimpleJsonEncodingStrategy()
prompt = strategy.encode(promptex)
print(prompt)
