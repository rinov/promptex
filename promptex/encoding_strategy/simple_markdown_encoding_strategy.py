from .base_encoding_strategy import BaseEncodingStrategy
from promptex import Promptex


class SimpleMarkdownEncodingStrategy(BaseEncodingStrategy):
    """
    Encode a promptex to a simple Markdown prompt
    """

    def encode(self, promptex: Promptex) -> str:
        if not promptex.elements:
            return ""
        markdown = ""
        for element in promptex.elements:
            markdown += self._encode_element(element, 1)
        return markdown

    def _encode_element(self, element, depth) -> str:
        encoded_text = ""
        encoded_text += f"{'#' * depth} {element.type.capitalize()}\n"
        encoded_text += f"{element.text}\n"

        if element.elements:
            sorted_child_elements = sorted(
                element.elements, key=lambda e: e.priority, reverse=True
            )
            for child in sorted_child_elements:
                encoded_text += f"\n{self._encode_element(child, depth + 1)}\n"

        return encoded_text
