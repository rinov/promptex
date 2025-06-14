import json
from typing import Dict, Any, List, TYPE_CHECKING
from .base_encoding_strategy import BaseEncodingStrategy

if TYPE_CHECKING:
    from ..promptex import Promptex
    from ..elements import Element


class SimpleJsonEncodingStrategy(BaseEncodingStrategy):
    """Encodes a Promptex object into a JSON string."""

    def encode(self, promptex: "Promptex") -> str:
        """
        Encodes the Promptex object into a JSON string.
        Elements are sorted by priority at the top level.
        """
        if not promptex.elements:
            return json.dumps([], indent=2, ensure_ascii=False)

        # Iterate directly over promptex.elements to preserve top-level order
        encoded_elements: List[Dict[str, Any]] = [
            self._encode_element(element) for element in promptex.elements
        ]
        return json.dumps(encoded_elements, indent=2, ensure_ascii=False)

    def _encode_element(self, element: "Element") -> Dict[str, Any]:
        """
        Recursively encodes an element and its children into a dictionary structure
        suitable for JSON serialization.
        """
        encoded_element: Dict[str, Any] = {
            "type": element.type,
            "text": element.text,
            "priority": element.priority, # Include priority
        }

        # Use the new get_sorted_children method
        child_elements = element.get_sorted_children()
        if child_elements:
            encoded_element["children"] = [ # Changed key from "elements" to "children" for clarity
                self._encode_element(child) for child in child_elements
            ]

        return encoded_element
