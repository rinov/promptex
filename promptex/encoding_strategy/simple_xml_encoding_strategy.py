from typing import TYPE_CHECKING
import xml.etree.ElementTree as ET # Standard import
from xml.dom.minidom import parseString # For pretty printing
import warnings # Import warnings module
from .base_encoding_strategy import BaseEncodingStrategy

if TYPE_CHECKING:
    from ..promptex import Promptex
    from ..elements import Element


class SimpleXmlEncodingStrategy(BaseEncodingStrategy):
    """Encodes a Promptex object into an XML string."""

    def encode(self, promptex: "Promptex") -> str:
        """
        Encodes the Promptex object into an XML string.
        Elements are sorted by priority at the top level.
        """
        if not promptex.elements:
            return ""

        root = ET.Element("promptex") # Changed root tag name

        # Iterate directly over promptex.elements to preserve top-level order
        for element in promptex.elements:
            self._encode_element(root, element)

        xml_str = ET.tostring(root, "utf-8")
        # Use minidom for pretty printing XML
        pretty_xml = parseString(xml_str).toprettyxml(indent="  ")
        return pretty_xml

    def _encode_element(self, parent_xml_element: ET.Element, element: "Element") -> None:
        """
        Recursively encodes an element and its children into XML elements,
        appending them to the parent XML element.
        """
        # Ensure element type is a valid XML tag name (basic sanitization)
        # More robust sanitization might be needed for arbitrary element types.
        tag_name = element.type.replace(" ", "_").replace(":", "_")
        try:
            xml_element = ET.SubElement(parent_xml_element, tag_name)
        except ValueError as e: # Handle invalid tag names if basic replace isn't enough
            warnings.warn(f"Invalid XML tag name '{tag_name}' from type '{element.type}'. Using 'element' instead. Error: {e}", UserWarning)
            xml_element = ET.SubElement(parent_xml_element, "element", attrib={"original_type": element.type})

        xml_element.text = element.text
        # Add priority as an attribute if it's non-zero (or always, if preferred)
        if element.priority != 0:
            xml_element.set("priority", str(element.priority))

        # Use the new get_sorted_children method
        for child in element.get_sorted_children():
            self._encode_element(xml_element, child)
