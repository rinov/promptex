from typing import TYPE_CHECKING
from .base_encoding_strategy import BaseEncodingStrategy

if TYPE_CHECKING:
    from ..promptex import Promptex
    from ..elements import Element


class SimpleTextEncodingStrategy(BaseEncodingStrategy):
    """Encodes a Promptex object into a plain text string with delimiters."""

    def __init__(
        self,
        separator: str = "\n\n", # Default to double newline for better separation
        delimiter: str = "---",  # Changed delimiter for common practice
        prefix_delimiter: bool = True, # Whether to add delimiter before type
    ) -> None:
        super().__init__()
        self.separator = separator
        self.delimiter = delimiter
        self.prefix_delimiter = prefix_delimiter

    def encode(self, promptex: "Promptex") -> str:
        """
        Encodes the Promptex object into a plain text string.
        Elements are sorted by priority at the top level.
        """
        if not promptex.elements:
            return ""

        text_parts = []
        # Iterate directly over promptex.elements to preserve top-level order
        for i, element in enumerate(promptex.elements):
            text_parts.append(self._encode_element(element))
            if i < len(promptex.elements) - 1: # Add separator if not the last element
                text_parts.append(self.separator)

        return "".join(text_parts)

    def _encode_element(self, element: "Element") -> str:
        """
        Recursively encodes an element and its children into a plain text string.
        """
        encoded_text_parts = []

        if self.prefix_delimiter:
            encoded_text_parts.append(f"{self.delimiter} {element.type.upper()} {self.delimiter}\n")
        else:
            encoded_text_parts.append(f"{element.type.upper()}\n")

        encoded_text_parts.append(f"{element.text}\n")

        # Use the new get_sorted_children method
        child_elements = element.get_sorted_children()
        if child_elements:
            # Add a small separator or indentation for children for clarity
            child_separator = self.separator # Could be different, e.g. "\n" + "  " for indent
            for i, child in enumerate(child_elements):
                encoded_text_parts.append(child_separator) # Separator before each child
                encoded_text_parts.append(self._encode_element(child)) # Recursive call

        return "".join(encoded_text_parts)
