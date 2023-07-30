import yaml
from .base_encoding_strategy import BaseEncodingStrategy
from promptex import Promptex


class SimpleYamlEncodingStrategy(BaseEncodingStrategy):
    """
    Encode a promptex to a simple YAML prompt
    """

    def encode(self, promptex: Promptex) -> str:
        if not promptex.elements:
            return ""
        yaml_dict = {}
        for element in promptex.elements:
            yaml_dict.update(self._encode_element(element))
        return yaml.dump(
            yaml_dict,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )

    def _encode_element(self, element) -> dict:
        encoded_dict = {}
        if element.elements:
            encoded_dict[element.type] = {
                "text": element.text,
                "children": [
                    self._encode_element(child) for child in element.elements
                ],
            }
        else:
            encoded_dict[element.type] = element.text

        return encoded_dict
