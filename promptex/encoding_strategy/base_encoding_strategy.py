from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..promptex import Promptex  # Use type checking for circular import


class BaseEncodingStrategy(ABC):
    @abstractmethod
    def encode(self, promptex: "Promptex") -> str:
        """
        Encodes the given Promptex object into a string representation.

        Args:
            promptex (Promptex): The Promptex object to encode.

        Returns:
            str: The encoded string representation of the prompt.
        """
        pass
