from .element_type import ElementType
from .element import Element


class Role(Element):
    def __init__(self, text: str):
        super().__init__(ElementType.ROLE.value, text)
