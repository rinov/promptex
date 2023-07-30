from .base_encoding_strategy import BaseEncodingStrategy
from promptex import Promptex


class SimpleHtmlEncodingStrategy(BaseEncodingStrategy):
    """
    Encode a promptex to a simple HTML prompt
    """

    def __init__(self):
        super().__init__()
        self.type_to_tag = {
            "instruction": "h1",
            "role": "h2",
            "constraint": "h3",
            "context": "p",
            "input_data": "p",
            "output_format": "p",
        }

    def encode(self, promptex: Promptex) -> str:
        if not promptex.elements:
            return ""
        html_list = []
        for element in promptex.elements:
            html_list.append(self._encode_element(element))
        return "<html>\n<body>\n" + "\n".join(html_list) + "\n</body>\n</html>"

    def _encode_element(self, element) -> str:
        tag = self.type_to_tag[element.type]
        html_str = f"<{tag}>{element.text}</{tag}>"

        if element.elements:
            sorted_child_elements = sorted(
                element.elements, key=lambda e: e.priority, reverse=True
            )
            for child in sorted_child_elements:
                html_str += self._encode_element(child)

        return html_str
