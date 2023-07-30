import json
from .base_encoding_strategy import BaseEncodingStrategy
from promptex import Promptex


class SimpleJsonEncodingStrategy(BaseEncodingStrategy):
    """
    Encode a promptex to a simple json prompt
    """

    def encode(self, promptex: Promptex) -> str:
        if not promptex.elements:
            return ""
        encoded_elements = [
            self._encode_element(element) for element in promptex.elements
        ]
        return json.dumps(encoded_elements, indent=2, ensure_ascii=False)

    def _encode_element(self, element) -> dict:
        encoded_element = {
            "type": element.type,
            "text": element.text,
        }

        if element.elements:
            sorted_child_elements = sorted(
                element.elements, key=lambda e: e.priority, reverse=True
            )
            encoded_element["elements"] = [
                self._encode_element(child) for child in sorted_child_elements
            ]

        return encoded_element
