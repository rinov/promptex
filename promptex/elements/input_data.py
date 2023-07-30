from .element_type import ElementType
from .element import Element


class InputData(Element):
    def __init__(self, text: str):
        super().__init__(ElementType.INPUT_DATA.value, text)
