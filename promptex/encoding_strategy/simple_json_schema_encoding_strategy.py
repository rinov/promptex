import json
from .base_encoding_strategy import BaseEncodingStrategy
from promptex import Promptex


class SimpleJsonSchemaEncodingStrategy(BaseEncodingStrategy):
    """
    Encode a promptex to a simple JSON schema
    """

    def __init__(self):
        super().__init__()

    def encode(self, promptex: Promptex) -> str:
        if not promptex.elements:
            return ""
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {},
            "required": [],
        }
        for element in promptex.elements:
            schema["properties"][element.type] = self._encode_element(element)
            schema["required"].append(element.type)
        return json.dumps(schema, indent=2, sort_keys=False)

    def _encode_element(self, element) -> dict:
        property_schema = {"type": "object", "properties": {}}

        if element.text:
            property_schema["properties"]["text"] = {"type": "string"}

        if element.elements:
            property_schema["properties"]["elements"] = {
                "type": "array",
                "items": [],
            }
            for child in element.elements:
                property_schema["properties"]["elements"]["items"].append(
                    self._encode_element(child)
                )

        return property_schema
