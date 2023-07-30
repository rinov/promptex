import sys
import os
import json

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

text = SimpleTextEncodingStrategy().encode(promptex)
encoding_model_name = "gpt-4"
token_count = promptex.get_token_count(
    text=text, encoding_model_name=encoding_model_name
)
stats = promptex.get_stats(text=text, encoding_model_name=encoding_model_name)

print(f"Token consumption: {token_count}")

print(f"Stats: {json.dumps(stats, indent=2, ensure_ascii=False)}")
