from .element_type import ElementType
from .element import Element


class Context(Element):
    def __init__(self, text: str):
        super().__init__(ElementType.CONTEXT.value, text)
