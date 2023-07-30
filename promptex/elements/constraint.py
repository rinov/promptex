from .element_type import ElementType
from .element import Element


class Constraint(Element):
    def __init__(self, text: str):
        super().__init__(ElementType.CONSTRAINT.value, text)
