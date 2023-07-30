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
        Role("You're a renowned RPG game designer."),
        Instruction(
            "Create an innovative quest for a new fantasy RPG game."
        ).add_elements(
            [
                Constraint(
                    "Ensure the quest is unique and rewarding for players."
                ),
            ]
        ),
        OutputFormat("Markdown text in English"),
    ]
)

strategy = SimpleTextEncodingStrategy()
prompt = strategy.encode(promptex)
print(prompt)
