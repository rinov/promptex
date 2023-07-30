import pickle
import logging
import tiktoken

from typing import List, Dict, Any
from collections import Counter


class Promptex:
    def __init__(self):
        self.elements = []
        self.logger = logging.getLogger(__name__)

    def __str__(self):
        return self.get_prompt_text()

    def clear(self):
        """
        Clear all elements
        """
        self.elements = []

    def add_elements(self, elements: List[str]):
        """
        Add elements to the prompt
        :param elements: The elements to add
        """
        self.elements.extend(elements)

    def set_elements(self, elements: List[str]):
        """
        Set elements to the prompt
        :param elements: The elements to set
        """
        self.elements = elements

    def save_prompt(self, filepath: str) -> None:
        """
        Save the prompt to a file
        :param filepath: The path to the file to save the prompt to
        """
        try:
            with open(filepath, "wb") as file:
                pickle.dump(self, file)
        except IOError as e:
            self.logger.error(f"Error saving promptex to file: {e}")
            raise e

    def load_prompt(self, filepath: str):
        """
        Load a prompt from a file
        :param filepath: The path to the file to load the prompt from
        :return: The loaded prompt
        """
        try:
            with open(filepath, "rb") as file:
                return pickle.load(file)
        except IOError as e:
            self.logger.error(f"Error loading prompt from file: {e}")
            raise e
        except pickle.UnpicklingError as e:
            logging.error(f"Error unpickling prompt from file: {e}")
            raise e

    def get_prompt(self, encoding_strategy) -> str:
        """
        Get the prompt
        :param encoding_strategy: The encoding strategy to use
        :return: The prompt
        """
        if not self.elements:
            raise ValueError("No elements to encode")

        return encoding_strategy.encode(self.elements)

    def get_token_count(self, text, encoding_model_name="gpt-4") -> int:
        """
        Get the token count of the prompt
        :seealso: https://github.com/openai/tiktoken/blob/main/tiktoken/model.py
        :param text: The text to get the token count
        :param encoding_model_name: gpt-4, gpt-3.5-turbo, text-davinci-001, etc..
        :return: The token count of the prompt
        """
        tiktoken_encoding = tiktoken.encoding_for_model(encoding_model_name)
        encoded = tiktoken_encoding.encode(text)
        token_count = len(encoded)
        return token_count

    def get_stats(self, text, encoding_model_name="gpt-4") -> Dict[str, Any]:
        """
        Get statistics about the elements in the prompt.
        :seealso: https://github.com/openai/tiktoken/blob/main/tiktoken/model.py
        :param text: The prompt text to get the statistics
        :param encoding_model_name: gpt-4, gpt-3.5-turbo, text-davinci-001, etc..
        :return: A dictionary with statistics
        """
        stats = {"element_count": {}, "text_length": {}, "token_count": {}}

        element_type_counter = Counter(
            [type(element).__name__ for element in self.elements]
        )
        stats["element_count"] = dict(element_type_counter)
        stats["element_count"]["total"] = len(self.elements)

        for element_type in stats["element_count"].keys():
            stats["text_length"][element_type] = {
                "min": 0,
                "max": 0,
                "avg": 0,
            }
            stats["token_count"][element_type] = {
                "min": 0,
                "max": 0,
                "avg": 0,
            }

        for element in self.elements:
            element_type = type(element).__name__
            token_count = self.get_token_count(text=element.text)
            text_length = len(element.text)

            stats["text_length"][element_type]["min"] = min(
                stats["text_length"][element_type]["min"], text_length
            )
            stats["text_length"][element_type]["max"] = max(
                stats["text_length"][element_type]["max"], text_length
            )
            stats["text_length"][element_type]["avg"] += text_length

            stats["token_count"][element_type]["min"] = min(
                stats["token_count"][element_type]["min"], token_count
            )
            stats["token_count"][element_type]["max"] = max(
                stats["token_count"][element_type]["max"], token_count
            )
            stats["token_count"][element_type]["avg"] += token_count

        if self.elements:
            for element_type in stats["element_count"].keys():
                stats["text_length"][element_type]["avg"] /= stats[
                    "element_count"
                ][element_type]
                stats["token_count"][element_type]["avg"] /= stats[
                    "element_count"
                ][element_type]

        stats["text_length"]["total"] = len(text)
        stats["token_count"]["total"] = self.get_token_count(
            text=text,
            encoding_model_name=encoding_model_name,
        )

        return stats
