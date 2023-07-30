from enum import Enum


class ElementType(Enum):
    """
    An Enum class that represents types of elements that make up the prompts in GPT models.

    Each Enum value represents the role of the element within the prompt and its priority.

    ROLE : An element that indicates the role of the prompt
    INSTRUCTION : An element that represents the instructions of the prompt
    CONSTRAINT : An element that represents the constraint conditions of the prompt
    CONTEXT : An element that provides the context or background information of the prompt
    INPUT_DATA : An element that represents the input data of the prompt
    OUTPUT_FORMAT : An element that represents the output format of the prompt
    """

    ROLE = "role", 1
    INSTRUCTION = "instruction", 2
    CONSTRAINT = "constraint", 3
    CONTEXT = "context", 4
    INPUT_DATA = "input_data", 5
    OUTPUT_FORMAT = "output_format", 6

    def __init__(self, value, priority):
        """
        :param value: The value of the Enum (a string representing the role of the prompt element)
        :param priority: The priority of the Enum (a number)
        """
        self._value_ = value
        self.priority = priority
