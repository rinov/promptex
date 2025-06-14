from typing import TYPE_CHECKING
from .base_encoding_strategy import BaseEncodingStrategy

if TYPE_CHECKING:
    from ..promptex import Promptex
    from ..elements import Element


class SimpleHtmlEncodingStrategy(BaseEncodingStrategy):
    """Encodes a Promptex object into an HTML string."""

    def __init__(self) -> None:
        super().__init__()
        # Default HTML tag mapping for element types
        self.type_to_tag = {
            "instruction": "h1",
            "role": "h2",
            "constraint": "h3",
            "context": "p",
            "input_data": "div",  # Using div for potential complex data
            "output_format": "pre", # Using pre for formatted output
            "default": "p", # Fallback tag
        }

    def encode(self, promptex: "Promptex") -> str:
        """
        Encodes the Promptex object into an HTML string.
        Elements are sorted by priority at the top level.
        """
        if not promptex.elements:
            return ""

        html_parts = []
        # Iterate directly over promptex.elements to preserve top-level order
        for element in promptex.elements:
            html_parts.append(self._encode_element(element))

        return f"<html>\n<head><title>Promptex Output</title></head>\n<body>\n{''.join(html_parts)}\n</body>\n</html>"

    def _encode_element(self, element: "Element") -> str:
        """
        Recursively encodes an element and its children into an HTML string.
        Child elements are nested within their parent's HTML structure.
        """
        tag = self.type_to_tag.get(element.type, self.type_to_tag["default"])

        # Sanitize text before putting it into HTML to prevent XSS if text can be arbitrary
        # For simplicity, basic escaping of < and >. A robust solution would use a library.
        safe_text = element.text.replace("<", "&lt;").replace(">", "&gt;")

        content = [f"<{tag}>{safe_text}"] # Content starts with the parent tag and its text

        # Use the new get_sorted_children method for child elements
        for child in element.get_sorted_children():
            content.append(self._encode_element(child)) # Append child HTML inside parent tag

        content.append(f"</{tag}>")
        return "\n".join(content)
