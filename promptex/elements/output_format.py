from .element_type import ElementType
from .element import Element


class OutputFormat(Element):
    def __init__(self, text: str):
        super().__init__(ElementType.OUTPUT_FORMAT.value, text)
