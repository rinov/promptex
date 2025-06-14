import json
from typing import Dict, Any, List, TYPE_CHECKING
from .base_encoding_strategy import BaseEncodingStrategy

if TYPE_CHECKING:
    from ..promptex import Promptex
    from ..elements import Element


class SimpleJsonSchemaEncodingStrategy(BaseEncodingStrategy):
    """
    Encodes a Promptex object into a JSON schema string.
    The schema represents the structure of the prompt elements.
    """

    def __init__(self) -> None:
        super().__init__()

    def encode(self, promptex: "Promptex") -> str:
        """
        Encodes the Promptex object into a JSON schema string.
        Top-level elements define the main properties of the schema.
        Order of top-level elements is preserved as in promptex.elements.
        """
        if not promptex.elements:
            return json.dumps({
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "properties": {},
            }, indent=2)

        schema: Dict[str, Any] = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": promptex.__class__.__name__ + " Schema", # Add a title
            "type": "object",
            "properties": {},
            "required": [],
        }

        # Order of top-level elements from promptex.elements is maintained
        # Sorting by priority is not applied here as schema definition order might be significant
        for element in promptex.elements:
            # Ensure element type is a string key
            element_type_key = str(element.type)
            schema["properties"][element_type_key] = self._encode_element(element)
            if element_type_key not in schema["required"]: # Avoid duplicate entries if types are repeated
                schema["required"].append(element_type_key)

        return json.dumps(schema, indent=2) # sort_keys=False is default for dicts in Python 3.7+

    def _encode_element(self, element: "Element") -> Dict[str, Any]:
        """
        Recursively encodes an element into a JSON schema property definition.
        Child elements are represented as an array of sub-schemas.
        The order of child elements is preserved as in element.elements (not sorted by priority).
        """
        property_schema: Dict[str, Any] = {
            "type": "object",
            "title": f"Element: {element.type}", # Add title for clarity
            "properties": {},
            "required": [] # Track required properties for this element
        }

        if element.text: # Check if text is not empty or None
            property_schema["properties"]["text"] = {"type": "string", "description": "Text content of the element"}
            property_schema["required"].append("text")


        # Child elements are processed in their original order (from element.elements)
        # Not using get_sorted_children() here, as schema might require specific order
        if element.elements:
            property_schema["properties"]["children"] = { # Changed key from "elements" to "children"
                "type": "array",
                "title": "Child Elements",
                "items": { # Assuming children could be of different types, more generic item schema
                           # Or provide a list of schemas if types are fixed per parent
                    "type": "object",
                    "title": "Child Element"
                }
            }
            # To be more precise, 'items' could be a list of schemas if children types are known
            # For now, a generic object. If specific child types are expected, this needs refinement.
            # Example for more specific items:
            # "items": [self._encode_element(child) for child in element.elements]
            # However, this creates a fixed list of item schemas, not "any of these"

            # A simpler approach for now: define child items generally.
            # If children always have the same structure, one could use:
            # "items": self._encode_element(element.elements[0]) if element.elements else {}
            # But this assumes all children are homogenous.

            # For heterogeneous children, oneOf/anyOf might be used if types are known:
            # "items": { "oneOf": [list of schemas for each child type] }

            # Current implementation keeps it simple: an array of generic objects for children.
            # This part might need more detailed requirements for a fully accurate schema.
            # For now, we'll represent children as an array of the same general element schema.
            # This means the schema will show 'children' as an array, and items within that
            # array will be elements encoded by this same _encode_element method.

            child_schemas = [self._encode_element(child) for child in element.elements]
            if child_schemas: # Only add 'children' property if there are actual child schemas
                items_schema = {"oneOf": child_schemas} if len(child_schemas) > 1 else child_schemas[0]
                property_schema["properties"]["children"] = {
                    "type": "array",
                    "title": "Child Elements",
                    "items": items_schema
                }
                property_schema["required"].append("children")

        if not property_schema["required"]: # If no sub-properties are required
            del property_schema["required"]

        return property_schema
