import csv
import io
from .base_encoding_strategy import BaseEncodingStrategy
from promptex import Promptex


class SimpleCsvEncodingStrategy(BaseEncodingStrategy):
    """
    Encode a promptex to a simple CSV prompt
    """

    def encode(self, promptex: Promptex) -> str:
        if not promptex.elements:
            return ""
        output = io.StringIO()
        writer = csv.writer(output)
        for element in promptex.elements:
            writer.writerow(self._encode_element(element))
        return output.getvalue()

    def _encode_element(self, element) -> list:
        encoded_element = [element.type.upper(), element.text]

        if element.elements:
            sorted_child_elements = sorted(
                element.elements, key=lambda e: e.priority, reverse=True
            )
            for child in sorted_child_elements:
                encoded_element.extend(self._encode_element(child))

        return encoded_element
