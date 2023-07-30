from .base_encoding_strategy import BaseEncodingStrategy
from promptex import Promptex
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString


class SimpleXmlEncodingStrategy(BaseEncodingStrategy):
    """
    Encode a promptex to a simple XML prompt
    """

    def encode(self, promptex: Promptex) -> str:
        if not promptex.elements:
            return ""
        root = Element("root")
        for element in promptex.elements:
            self._encode_element(root, element)
        xml_str = tostring(root, "utf-8")
        pretty_xml = parseString(xml_str).toprettyxml(indent="  ")
        return pretty_xml

    def _encode_element(self, parent_xml_element, element):
        xml_element = SubElement(parent_xml_element, element.type)
        xml_element.text = element.text

        if element.elements:
            sorted_child_elements = sorted(
                element.elements, key=lambda e: e.priority, reverse=True
            )
            for child in sorted_child_elements:
                self._encode_element(xml_element, child)
