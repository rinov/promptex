from .element_type import ElementType
from .element import Element


class Instruction(Element):
    def __init__(self, text: str):
        super().__init__(ElementType.INSTRUCTION.value, text)
