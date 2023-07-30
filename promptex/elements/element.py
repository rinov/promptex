from .element_type import ElementType
from typing import Dict


class Element:
    def __init__(self, type: str, text: str, priority: int = 0):
        """
        Args:
            type (ElementType): Type of the element
            text (str): Text of the element
            priority (int, optional): Priority of the element. Defaults to 0.
        """
        self.type = type
        self.text = text
        self.elements = []
        self.priority = priority

    def __eq__(self, other):
        if not isinstance(other, Element):
            return NotImplemented

        return (
            self.type == other.type
            and self.text == other.text
            and self.priority == other.priority
        )

    def clear_child_elements(self):
        self.elements = []

    def add_element(self, element) -> "Element":
        self.elements.append(element)
        return self

    def add_elements(self, elements) -> "Element":
        self.elements.extend(elements)
        return self

    def to_dict(self) -> Dict[str, str]:
        if self.elements:
            data = {"text": self.text}
            for element_type in ElementType:
                elements_of_type = [
                    element.text
                    for element in self.elements
                    if element.type == element_type
                ]
                if elements_of_type:
                    data[element_type] = elements_of_type
            return {self.type: data}
        else:
            return {self.type: self.text}
