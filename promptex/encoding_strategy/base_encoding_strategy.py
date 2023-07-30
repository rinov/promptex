from abc import ABC, abstractmethod
from promptex import Promptex


class BaseEncodingStrategy(ABC):
    @abstractmethod
    def encode(self, promptex: Promptex) -> str:
        """
        Encode a list of elements into a string.

        Args:
            elements (List[Element]): List of elements to encode.

        Returns:
            str: Encoded string.
        """
        pass
