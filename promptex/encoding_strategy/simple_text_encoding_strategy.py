from .base_encoding_strategy import BaseEncodingStrategy
from promptex import Promptex


class SimpleTextEncodingStrategy(BaseEncodingStrategy):
    """
    Encode a promptex to a simple text prompt
    """

    def __init__(
        self,
        separator: str = "\n",
        delimiter: str = "#",
        delimiter_count: int = 3,
    ):
        super().__init__()
        self.separator = separator
        self.delimiter = delimiter
        self.delimiter_count = delimiter_count

    def encode(self, promptex: Promptex) -> str:
        if not promptex.elements:
            return ""
        prompt = ""
        for element in promptex.elements:
            prompt += self._encode_element(element)
        return prompt

    def _encode_element(self, element) -> str:
        encoded_text = ""
        delimiter_str = self.delimiter * self.delimiter_count
        encoded_text += f"\n{delimiter_str} {element.type.upper()}\n{element.text}\n{delimiter_str}\n"

        if element.elements:
            sorted_child_elements = sorted(
                element.elements, key=lambda e: e.priority, reverse=True
            )
            for child in sorted_child_elements:
                encoded_text += f"\n{self._encode_element(child)}\n"

        return encoded_text
