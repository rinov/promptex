# Promptex

Promptex is a Python library built for efficient and effective management of prompts utilized in Generative Pre-trained Transformer (GPT) models. Whether you're a researcher or a developer, this tool offers an easy way to manage, integrate, and analyze your prompts.

## Key Features

- **Prompt Management**: Provides methods to set up and get prompts, allowing for flexibility to match your unique needs.
- **Data Integration**: Supports a wide array of file formats (JSON, JSON Schema, CSV, XML, YAML, HTML) for seamless integration into your data pipeline.
- **Analytics**: Equips you with the ability to gather detailed statistics about the elements in your prompts, such as text length and token count, valuable for fine-tuning your model.
- **Scalability**: Designed with large-scale projects in mind, ensuring efficiency regardless of the size of your GPT-based projects.

By offering this wide range of functionalities, Promptex provides a flexible and efficient way to work with prompts in transformer models. Join us on this journey towards making GPT prompt handling simpler, more efficient, and effective!

## Why is Prompt Management and Analysis Necessary?

Generative Pre-trained Transformer (GPT) models and the like generate output based on input prompts. Prompts serve as essential cues that instruct the model what to generate, and the selection and management of these prompts significantly impact the quality and relevance of the results.

Moreover, efficiently managing prompts used in projects or research is crucial to ensure consistency and reproducibility. Promptex addresses these challenges, and by understanding not just the meaning of the sentences, but also the characteristics of the prompts, such as their composition and token count, it provides opportunities to maximize the performance of GPT models.

Therefore, effective prompt management and analysis not only aid in producing better and more consistent results but also pave the way to harness the full potential of GPT models.

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

## Prompt Components

In Promptex, Some of fundamental elements that make up a prompt for Generative Pre-trained Transformer (GPT) models. These elements, each with a specific role and priority, form the building blocks for creating effective prompts:

ROLE: This element indicates the role of the prompt.
INSTRUCTION: This element provides specific instructions to guide the GPT model's response.
CONSTRAINT: This element defines any constraints or limitations that the GPT model should adhere to while generating a response.
CONTEXT: This element gives the context or background information necessary for understanding the prompt.
INPUT_DATA: This element represents the specific input data that the GPT model needs to generate a response.
OUTPUT_FORMAT: This element specifies the desired format of the model's output.


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


Token consumption: 27
Stats: {
  "element_count": {
    "Instruction": 1,
    "OutputFormat": 1,
    "total": 2
  },
  "text_length": {
    "Instruction": {
      "min": 0,
      "max": 54,
      "avg": 54.0
    },
    "OutputFormat": {
      "min": 0,
      "max": 24,
      "avg": 24.0
    },
    "total": 124
  },
  "token_count": {
    "Instruction": {
      "min": 0,
      "max": 11,
      "avg": 11.0
    },
    "OutputFormat": {
      "min": 0,
      "max": 4,
      "avg": 4.0
    },
    "total": 27
  }
}
```

### Encoding a prompt as JSON
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

### Encoding a prompt as XML
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

### Encoding a prompt as JSON Schema
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
