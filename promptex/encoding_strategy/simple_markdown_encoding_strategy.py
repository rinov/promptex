from typing import TYPE_CHECKING
from .base_encoding_strategy import BaseEncodingStrategy

if TYPE_CHECKING:
    from ..promptex import Promptex
    from ..elements import Element


class SimpleMarkdownEncodingStrategy(BaseEncodingStrategy):
    """Encodes a Promptex object into a Markdown string."""

    def encode(self, promptex: "Promptex") -> str:
        """
        Encodes the Promptex object into a Markdown string.
        Elements are sorted by priority at the top level.
        """
        if not promptex.elements:
            return ""

        markdown_parts = []
        # Iterate directly over promptex.elements to preserve top-level order
        for element in promptex.elements:
            markdown_parts.append(self._encode_element(element, 1))

        return "".join(markdown_parts)

    def _encode_element(self, element: "Element", depth: int) -> str:
        """
        Recursively encodes an element and its children into a Markdown string.
        Uses heading levels based on depth.
        """
        # Ensure depth is within a reasonable range for Markdown headings (1-6)
        effective_depth = max(1, min(depth, 6))

        encoded_text_parts = [
            f"{'#' * effective_depth} {element.type.capitalize()}\n",
            f"{element.text}\n\n" # Add extra newline for spacing after text
        ]

        # Use the new get_sorted_children method
        for child in element.get_sorted_children():
            encoded_text_parts.append(self._encode_element(child, effective_depth + 1))

        return "".join(encoded_text_parts)
