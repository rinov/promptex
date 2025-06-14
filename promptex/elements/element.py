from .element_type import ElementType
from typing import Dict, List, Any


class Element:
    elements: List["Element"]  # Type hint for instance variable

    def __init__(self, type: str, text: str, priority: int = 0):
        """
        Args:
            type (str): Type of the element (e.g., "role", "instruction").
            text (str): Text content of the element.
            priority (int, optional): Priority for ordering. Defaults to 0.
        """
        self.type = type
        self.text = text
        self.elements = []
        self.priority = priority

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Element):
            return NotImplemented

        return (
            self.type == other.type
            and self.text == other.text
            and self.priority == other.priority
        )

    def clear_child_elements(self) -> None:
        self.elements = []

    def add_element(self, element: "Element") -> "Element":
        """Adds a child element."""
        self.elements.append(element)
        return self

    def add_elements(self, elements: List["Element"]) -> "Element":
        """Adds multiple child elements."""
        self.elements.extend(elements)
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Converts the element and its children to a dictionary."""
        if self.elements:
            data: Dict[str, Any] = {"text": self.text}
            # Group child elements by their type
            for child_element in self.elements:
                # Ensure child_element.type is a string, which is expected here
                # as ElementType values are strings.
                type_key = child_element.type
                if type_key not in data:
                    data[type_key] = []

                # Add child's text or its full dict if it also has children
                child_dict = child_element.to_dict()
                # We want the inner value part of the child's dict
                data[type_key].append(child_dict[child_element.type])

            return {self.type: data}
        else:
            return {self.type: self.text}

    def get_sorted_children(self) -> List["Element"]:
        """Returns child elements sorted by priority (descending)."""
        return sorted(self.elements, key=lambda e: e.priority, reverse=True)
