import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from promptex.promptex import Promptex
from promptex.elements import *
from promptex.encoding_strategy import *


# Add a new encoding strategy
class BinaryEncodingStrategy(BaseEncodingStrategy):
    def __init__(self):
        super().__init__()

    def encode(self, promptex: Promptex) -> bytes:
        prompt = ""
        for element in promptex.elements:
            prompt += element.text
        return prompt.encode()


promptex = Promptex()

promptex.set_elements([Instruction("Create a new fantasy RPG game.")])

strategy = BinaryEncodingStrategy()
prompt = strategy.encode(promptex)
print(prompt)
