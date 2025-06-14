from enum import Enum


class ElementType(Enum):
    """Defines types of elements for GPT prompts, including their role and priority."""

    ROLE = "role", 1
    INSTRUCTION = "instruction", 2
    CONSTRAINT = "constraint", 3
    CONTEXT = "context", 4
    INPUT_DATA = "input_data", 5
    OUTPUT_FORMAT = "output_format", 6

    def __init__(self, value: str, priority: int):
        self._value_ = value
        self.priority = priority
