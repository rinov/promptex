import csv
import io
from typing import List, TYPE_CHECKING
from .base_encoding_strategy import BaseEncodingStrategy

if TYPE_CHECKING:
    from ..promptex import Promptex
    from ..elements import Element


class SimpleCsvEncodingStrategy(BaseEncodingStrategy):
    """Encodes a Promptex object into a CSV string."""

    def encode(self, promptex: "Promptex") -> str:
        """
        Encodes the Promptex object into a CSV string.
        Each element and its children are represented as rows.
        """
        if not promptex.elements:
            return ""
        output = io.StringIO()
        writer = csv.writer(output)
        # Iterate directly over promptex.elements to preserve top-level order
        for element in promptex.elements:
            writer.writerow(self._encode_element(element))
        return output.getvalue().strip() # Strip trailing newline

    def _encode_element(self, element: "Element") -> List[str]:
        """
        Recursively encodes an element and its children into a list of strings
        for a CSV row. Child elements are appended to the same row.
        """
        encoded_element_parts = [element.type.upper(), element.text]

        # Use the new get_sorted_children method
        for child in element.get_sorted_children():
            # Child elements are flattened into the same row
            encoded_element_parts.extend(self._encode_element(child))

        return encoded_element_parts
