import yaml
from typing import Dict, Any, List, TYPE_CHECKING
from .base_encoding_strategy import BaseEncodingStrategy

if TYPE_CHECKING:
    from ..promptex import Promptex
    from ..elements import Element


class SimpleYamlEncodingStrategy(BaseEncodingStrategy):
    """Encodes a Promptex object into a YAML string."""

    def encode(self, promptex: "Promptex") -> str:
        """
        Encodes the Promptex object into a YAML string.
        Elements are sorted by priority at the top level.
        The output is a list of element representations.
        """
        if not promptex.elements:
            return yaml.dump([], default_flow_style=False, allow_unicode=True)

        # Iterate directly over promptex.elements to preserve top-level order
        # The top-level structure will be a list of encoded elements
        encoded_list: List[Dict[str, Any]] = [
            self._encode_element(element) for element in promptex.elements
        ]

        return yaml.dump(
            encoded_list,
            default_flow_style=False,
            sort_keys=False, # Keep order from list
            allow_unicode=True,
            indent=2 # Add indentation for readability
        )

    def _encode_element(self, element: "Element") -> Dict[str, Any]:
        """
        Recursively encodes an element and its children into a dictionary structure
        suitable for YAML serialization. Each element is represented as a dictionary
        with its type as the key.
        """
        content: Dict[str, Any] = {"text": element.text}

        # Use the new get_sorted_children method
        child_elements = element.get_sorted_children()
        if child_elements:
            content["children"] = [
                self._encode_element(child) for child in child_elements
            ]

        # The element itself is represented as a dictionary with its type as the key
        # and its content (text, children) as the value.
        return {element.type: content}
