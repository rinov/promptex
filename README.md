# Promptex

Promptex is a Python library specially crafted to simplify the handling of prompts used as inputs for Generative Pre-trained Transformer (GPT) models. It empowers researchers and developers to manage prompts effectively and efficiently.

This framework plays a significant role in the fundamental research that aims to develop new architectures for foundation models and AGI. It concentrates on improving the generality and capability of these models and enhancing their training stability and efficiency.

## Core Focuses

- **Flexibility**: Promptex provides methods to easily add, set, clear, and get prompts, giving you the ability to tailor the prompt setup to suit your unique requirements.
- **Data Integration**: It supports various file formats like JSON, JSON Schema, CSV, XML, YAML, and HTML for saving and loading prompts, ensuring seamless integration with your data pipeline.
- **Analytics**: The library provides a method to gather detailed statistics about the elements in your prompts, such as text length and token count. This feature can be very beneficial for fine-tuning your model.
- **Scalability**: Promptex is designed with efficiency and scalability in mind, making it an ideal tool for managing prompts in large-scale GPT-based projects.

## Key Features

- **Prompt Management**: Easily add, set, clear, and get prompts.
- **File Handling**: Save and load prompts from files. It supports various formats such as JSON, CSV, XML, YAML, and HTML.
- **Stats Collection**: Obtain statistics about the elements in the prompt. This includes details such as the count, length, and token count of each element.

By offering this wide range of functionalities, Promptex provides a flexible and efficient way to work with prompts in transformer models. Join us on this journey towards making GPT prompt handling simpler, more efficient, and effective!

## Installation

To install:

```bash
pip install -U pip
pip install promptex
```

Alternatively, you can develop it locally:

```bash
git clone https://github.com/rinov/promptex.git
cd promptex
pip install -e .
```

## Getting Started
```python
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

"""
### ROLE
You're a renowned RPG game designer.
###

### INSTRUCTION
Create an innovative quest for a new fantasy RPG game.
###

### CONSTRAINT
Ensure the quest is unique and rewarding for players.
###

### OUTPUT_FORMAT
Markdown text in English
###
"""
```

## Examples
For a more detailed understanding and hands-on experience, please refer to the "examples" directory.

### Manage your prompt
```python
path = "examples/test.json"

# Save the prompt to a file
promptex.save_prompt(path)

# Load the prompt from a file
promptex = promptex.load_prompt(path)
```

### Show stats of prompt
```python
path = "examples/test.json"

# Save the prompt to a file
promptex.save_prompt(path)

# Load the prompt from a file
promptex = promptex.load_prompt(path)
```

### Encoding a promt as JSON
```python
strategy = SimpleJsonEncodingStrategy()
prompt = strategy.encode(promptex)
print(prompt)

"""
[
  {
    "type": "role",
    "text": "You're a renowned RPG game designer."
  },
  {
    "type": "instruction",
    "text": "Create an innovative quest for a new fantasy RPG game.",
    "elements": [
      {
        "type": "constraint",
        "text": "Ensure the quest is unique and rewarding for players."
      }
    ]
  },
  {
    "type": "output_format",
    "text": "Markdown text in English"
  }
]
"""
```

### Encoding a promt as XML
```python
strategy = SimpleXmlEncodingStrategy()
prompt = strategy.encode(promptex)
print(prompt)

"""
<?xml version="1.0" ?>
<root>
  <role>You're a renowned RPG game designer.</role>
  <instruction>
    Create an innovative quest for a new fantasy RPG game.
    <constraint>Ensure the quest is unique and rewarding for players.</constraint>
  </instruction>
  <output_format>Markdown text in English</output_format>
</root>
"""
```

### Encoding a promt as JSON Schema
```python
strategy = SimpleXmlEncodingStrategy()
prompt = strategy.encode(promptex)
print(prompt)

"""
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "role": {
      "type": "object",
      "properties": {
        "text": {
          "type": "string"
        }
      }
    },
    "instruction": {
      "type": "object",
      "properties": {
        "text": {
          "type": "string"
        },
        "elements": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "properties": {
                "text": {
                  "type": "string"
                }
              }
            }
          ]
        }
      }
    },
    "output_format": {
      "type": "object",
      "properties": {
        "text": {
          "type": "string"
        }
      }
    }
  },
  "required": [
    "role",
    "instruction",
    "output_format"
  ]
}
"""
```

### Customize encoding strategy
```python
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
```

### Setup your element type
```python

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
```

## Contribute
We welcome all contributions. Feel free to submit a pull request or open an issue on our GitHub page.

## LICENSE
Promptex is licensed under the MIT license. For more information, see the LICENSE file.
