import pickle
import logging
import tiktoken

from typing import List, Dict, Any
from collections import Counter
from .elements import Element  # Added import
from .encoding import BaseEncodingStrategy, SimpleTextEncodingStrategy  # Added imports


class Promptex:
    def __init__(self) -> None:
        self.elements: List[Element] = []  # Type hint added
        self.logger = logging.getLogger(__name__)

    def __str__(self) -> str:
        """Returns a simple text representation of the prompt."""
        return self.get_prompt(SimpleTextEncodingStrategy())

    def clear(self) -> None:
        """Clears all elements from the prompt."""
        self.elements = []

    def add_elements(self, elements: List[Element]) -> None:
        """
        Adds multiple elements to the prompt.
        :param elements: A list of Element objects to add.
        """
        self.elements.extend(elements)

    def set_elements(self, elements: List[Element]) -> None:
        """
        Sets the elements of the prompt, replacing any existing elements.
        :param elements: A list of Element objects to set.
        """
        self.elements = elements

    def save_prompt(self, filepath: str) -> None:
        """
        Saves the Promptex object to a file using pickle.
        :param filepath: The path to the file.
        """
        try:
            with open(filepath, "wb") as file:
                pickle.dump(self, file)
        except IOError as e:
            self.logger.error(f"Error saving promptex to file: {e}")
            raise

    @classmethod
    def load_prompt(cls, filepath: str) -> "Promptex":
        """
        Loads a Promptex object from a file.
        :param filepath: The path to the file.
        :return: The loaded Promptex object.
        """
        try:
            with open(filepath, "rb") as file:
                return pickle.load(file)
        except IOError as e:
            cls().logger.error(f"Error loading prompt from file: {e}") # Use cls() to get logger if needed before instance
            raise
        except pickle.UnpicklingError as e:
            cls().logger.error(f"Error unpickling prompt from file: {e}") # Use cls() for logger
            raise

    def get_prompt(self, encoding_strategy: BaseEncodingStrategy) -> str:
        """
        Encodes the prompt using the provided encoding strategy.
        :param encoding_strategy: The encoding strategy to use.
        :return: The encoded prompt as a string.
        """
        if not self.elements:
            self.logger.warning("No elements to encode, returning empty string.")
            return ""
        return encoding_strategy.encode(self) # Pass self instead of self.elements

    def get_token_count(self, text: str, encoding_model_name: str = "gpt-4") -> int:
        """
        Calculates the token count for a given text using tiktoken.
        :seealso: https://github.com/openai/tiktoken/blob/main/tiktoken/model.py
        :param text: The text to tokenize.
        :param encoding_model_name: Model name for tiktoken (e.g., gpt-4, gpt-3.5-turbo).
        :return: The number of tokens.
        """
        try:
            tiktoken_encoding = tiktoken.encoding_for_model(encoding_model_name)
            encoded = tiktoken_encoding.encode(text)
            return len(encoded)
        except Exception as e:
            self.logger.error(f"Error getting token count: {e}")
            return 0

    def get_stats(self, encoding_model_name: str = "gpt-4") -> Dict[str, Any]:
        """
        Calculates statistics about the elements in the prompt.
        Statistics include element counts, text lengths (min, max, avg),
        and token counts (min, max, avg) per element type and for the total prompt.
        :param encoding_model_name: Model name for tiktoken (e.g., gpt-4).
        :return: A dictionary containing the statistics.
        """
        if not self.elements:
            return {
                "element_count": {"total": 0},
                "text_length": {"total": 0},
                "token_count": {"total": 0},
            }

        stats: Dict[str, Any] = {
            "element_count": {},
            "text_length": {},
            "token_count": {},
        }

        # Calculate per-element stats
        element_type_counter = Counter(element.type for element in self.elements)
        stats["element_count"] = dict(element_type_counter)

        # Initialize min/max/sum structures for text length and token count per type
        for element_type_val in element_type_counter.keys():
            stats["text_length"][element_type_val] = {
                "min": float('inf'), "max": float('-inf'), "sum": 0, "avg": 0
            }
            stats["token_count"][element_type_val] = {
                "min": float('inf'), "max": float('-inf'), "sum": 0, "avg": 0
            }

        for element in self.elements:
            element_type_val = element.type # Use element.type (string)
            text_length = len(element.text)
            token_count = self.get_token_count(
                text=element.text, encoding_model_name=encoding_model_name
            )

            # Text length stats
            stats["text_length"][element_type_val]["min"] = min(
                stats["text_length"][element_type_val]["min"], text_length
            )
            stats["text_length"][element_type_val]["max"] = max(
                stats["text_length"][element_type_val]["max"], text_length
            )
            stats["text_length"][element_type_val]["sum"] += text_length

            # Token count stats
            stats["token_count"][element_type_val]["min"] = min(
                stats["token_count"][element_type_val]["min"], token_count
            )
            stats["token_count"][element_type_val]["max"] = max(
                stats["token_count"][element_type_val]["max"], token_count
            )
            stats["token_count"][element_type_val]["sum"] += token_count

        # Calculate averages
        for element_type_val, count in element_type_counter.items():
            if count > 0:
                stats["text_length"][element_type_val]["avg"] = (
                    stats["text_length"][element_type_val]["sum"] / count
                )
                stats["token_count"][element_type_val]["avg"] = (
                    stats["token_count"][element_type_val]["sum"] / count
                )
            # Clean up sum
            del stats["text_length"][element_type_val]["sum"]
            del stats["token_count"][element_type_val]["sum"]


        # Calculate total prompt text and token count
        # Using SimpleTextEncodingStrategy as a default for overall stats
        total_prompt_text = self.get_prompt(SimpleTextEncodingStrategy())
        stats["text_length"]["total"] = len(total_prompt_text)
        stats["token_count"]["total"] = self.get_token_count(
            text=total_prompt_text, encoding_model_name=encoding_model_name
        )
        stats["element_count"]["total"] = len(self.elements)

        return stats
