import pytest

from promptex import Promptex
from promptex.elements import *


@pytest.fixture
def role():
    return Role("Role")


@pytest.fixture
def instruction():
    return Instruction("Instruction")


@pytest.fixture
def constraint():
    return Constraint("Constraint")


@pytest.fixture
def context():
    return Context("Context")


@pytest.fixture
def input_data():
    return InputData("InputData")


@pytest.fixture
def output_format():
    return OutputFormat("OutputFormat")


def test_role(role):
    assert role.text == "Role"
    assert role.type == "role"
    assert role.to_dict() == {"role": "Role"}


def test_instruction(instruction):
    assert instruction.text == "Instruction"
    assert instruction.type == "instruction"
    assert instruction.to_dict() == {"instruction": "Instruction"}


def test_constraint(constraint):
    assert constraint.text == "Constraint"
    assert constraint.type == "constraint"
    assert constraint.to_dict() == {"constraint": "Constraint"}


def test_context(context):
    assert context.text == "Context"
    assert context.type == "context"
    assert context.to_dict() == {"context": "Context"}


def test_input_data(input_data):
    assert input_data.text == "InputData"
    assert input_data.type == "input_data"
    assert input_data.to_dict() == {"input_data": "InputData"}


def test_output_format(output_format):
    assert output_format.text == "OutputFormat"
    assert output_format.type == "output_format"
    assert output_format.to_dict() == {"output_format": "OutputFormat"}


def test_promptex(role, instruction, output_format):
    promptex = Promptex()
    promptex.add_elements([role, instruction, output_format])

    assert len(promptex.elements) == 3


# Tests for ElementType
from promptex.elements.element_type import ElementType

def test_element_type_priorities():
    assert ElementType.ROLE.priority == 1
    assert ElementType.INSTRUCTION.priority == 2
    assert ElementType.CONSTRAINT.priority == 3
    assert ElementType.CONTEXT.priority == 4
    assert ElementType.INPUT_DATA.priority == 5
    assert ElementType.OUTPUT_FORMAT.priority == 6


# Tests for Element Class

def test_element_creation_with_priority():
    element = Element("test_type", "test_text", priority=10)
    assert element.type == "test_type"
    assert element.text == "test_text"
    assert element.priority == 10

def test_add_single_child_element():
    parent = Element("parent", "parent_text")
    child = Element("child", "child_text")
    parent.add_element(child)
    assert child in parent.elements
    assert len(parent.elements) == 1

def test_add_multiple_child_elements():
    parent = Element("parent", "parent_text")
    child1 = Element("child1", "text1")
    child2 = Element("child2", "text2")
    parent.add_elements([child1, child2])
    assert child1 in parent.elements
    assert child2 in parent.elements
    assert len(parent.elements) == 2

def test_clear_child_elements():
    parent = Element("parent", "parent_text")
    child = Element("child", "child_text")
    parent.add_element(child)
    assert len(parent.elements) == 1
    parent.clear_child_elements()
    assert len(parent.elements) == 0

def test_get_sorted_children():
    parent = Element("parent", "parent_text")
    child1 = Element("child_high_priority", "text1", priority=10)
    child2 = Element("child_low_priority", "text2", priority=1)
    child3 = Element("child_mid_priority", "text3", priority=5)

    parent.add_elements([child2, child1, child3]) # Add in non-sorted order

    sorted_children = parent.get_sorted_children()
    assert len(sorted_children) == 3
    assert sorted_children[0] == child1
    assert sorted_children[1] == child3
    assert sorted_children[2] == child2
    # Verify original list is not mutated if get_sorted_children returns a new list
    assert parent.elements[0] == child2
    assert parent.elements[1] == child1
    assert parent.elements[2] == child3


def test_element_equality():
    el1 = Element("type1", "text1", priority=1)
    el2 = Element("type1", "text1", priority=1)
    el3 = Element("type2", "text1", priority=1) # Different type
    el4 = Element("type1", "text2", priority=1) # Different text
    el5 = Element("type1", "text1", priority=2) # Different priority

    child = Element("child", "child_text")
    el1_with_child = Element("type1", "text1", priority=1)
    el1_with_child.add_element(child)

    assert el1 == el2
    assert el1 != el3
    assert el1 != el4
    assert el1 != el5
    assert el1 != "not_an_element" # Comparison with non-element
    assert (el1 == el1_with_child) # __eq__ does not consider children

def test_element_to_dict_simple_with_priority():
    # Tests an element with no children and non-default priority.
    # The current Element.to_dict() does not include priority for simple elements.
    el = Element("custom_type", "custom_text", priority=5)
    assert el.to_dict() == {"custom_type": "custom_text"}

def test_element_to_dict_with_children():
    parent = Element("parent_type", "parent_text", priority=1)
    child1 = Element("child_type_A", "child1_A_text", priority=3)
    child2 = Element("child_type_B", "child2_B_text", priority=2)
    child3 = Element("child_type_A", "child3_A_text", priority=1) # Same type as child1

    parent.add_elements([child1, child2, child3])

    expected_dict = {
        "parent_type": {
            "text": "parent_text",
            # Children are grouped by type, and their .to_dict() output is used.
            # Since these children are simple, it's their text.
            "child_type_A": ["child1_A_text", "child3_A_text"],
            "child_type_B": ["child2_B_text"],
        }
    }
    # Note: The order of keys like "child_type_A" vs "child_type_B" in the dict
    # might not be guaranteed by default in older Pythons, but for testing it should be consistent.
    # The order of items within "child_type_A" list depends on original add_elements order
    # if not sorted by to_dict internally (which it is not, it iterates self.elements).
    # The current to_dict iterates self.elements (which is insertion order for children),
    # then groups them. So, the order within the list for "child_type_A" should be child1 then child3.

    actual_dict = parent.to_dict()
    assert actual_dict["parent_type"]["text"] == "parent_text"
    # Direct comparison for child_type_A as their insertion order is preserved by to_dict for children of the same type
    assert actual_dict["parent_type"]["child_type_A"] == ["child1_A_text", "child3_A_text"]
    assert actual_dict["parent_type"]["child_type_B"] == ["child2_B_text"]
    # Check all keys are present
    assert "text" in actual_dict["parent_type"]
    assert "child_type_A" in actual_dict["parent_type"]
    assert "child_type_B" in actual_dict["parent_type"]


def test_element_to_dict_with_nested_children():
    root = Element("root", "root_text")
    parent1 = Element("parent1", "p1_text", priority=2)
    child1_1 = Element("c1_1", "c1_1_text")
    child1_2 = Element("c1_2", "c1_2_text")
    parent1.add_elements([child1_1, child1_2])

    parent2 = Element("parent2", "p2_text", priority=1) # Simple parent, no children

    root.add_elements([parent1, parent2])

    expected_dict = {
        "root": {
            "text": "root_text",
            "parent1": [ # parent1 has children, so its entry is a list of its dict representation
                {
                    "text": "p1_text",
                    "c1_1": ["c1_1_text"],
                    "c1_2": ["c1_2_text"]
                }
            ],
            "parent2": ["p2_text"] # parent2 is simple, so its entry is a list of its text
        }
    }
    actual_dict = root.to_dict()
    # To avoid issues with list order within dict for multiple children of same type (though not in this specific test case for root's direct children types)
    # and key order in general for older python versions for the inner dicts.
    assert actual_dict["root"]["text"] == expected_dict["root"]["text"]
    assert actual_dict["root"]["parent2"] == expected_dict["root"]["parent2"]

    # Detailed check for parent1's structure
    assert len(actual_dict["root"]["parent1"]) == 1
    parent1_dict_actual = actual_dict["root"]["parent1"][0]
    expected_parent1_dict = expected_dict["root"]["parent1"][0]

    assert parent1_dict_actual["text"] == expected_parent1_dict["text"]
    assert sorted(parent1_dict_actual["c1_1"]) == sorted(expected_parent1_dict["c1_1"])
    assert sorted(parent1_dict_actual["c1_2"]) == sorted(expected_parent1_dict["c1_2"])
    assert sorted(parent1_dict_actual.keys()) == sorted(expected_parent1_dict.keys())

    # Check all keys are present at root level
    assert sorted(actual_dict["root"].keys()) == sorted(expected_dict["root"].keys())


# Tests for Promptex Class
import tempfile
import os
from unittest.mock import MagicMock, patch
from promptex.encoding import SimpleTextEncodingStrategy, BaseEncodingStrategy

def test_promptex_initialization():
    promptex = Promptex()
    assert promptex.elements == []
    assert promptex.logger is not None

def test_promptex_add_elements(role, instruction, context):
    promptex = Promptex()
    elements_to_add = [role, instruction]
    promptex.add_elements(elements_to_add)
    assert promptex.elements == elements_to_add

    promptex.add_elements([context])
    assert promptex.elements == elements_to_add + [context]

def test_promptex_set_elements(role, instruction, context):
    promptex = Promptex()
    promptex.add_elements([role])
    new_elements = [instruction, context]
    promptex.set_elements(new_elements)
    assert promptex.elements == new_elements

def test_promptex_clear_elements(role, instruction):
    promptex = Promptex()
    promptex.add_elements([role, instruction])
    promptex.clear()
    assert promptex.elements == []

def test_promptex_save_and_load_prompt():
    promptex_original = Promptex()
    el1 = Role("User Role")
    el2 = Instruction("Do this")
    el_child = Context("context text")
    el2.add_element(el_child) # Test with child element
    promptex_original.add_elements([el1, el2])

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as tmp_file:
        filepath = tmp_file.name

    try:
        promptex_original.save_prompt(filepath)
        promptex_loaded = Promptex.load_prompt(filepath)
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    assert isinstance(promptex_loaded, Promptex)
    assert len(promptex_loaded.elements) == len(promptex_original.elements)
    for i in range(len(promptex_original.elements)):
        assert promptex_loaded.elements[i] == promptex_original.elements[i]
        # Element.__eq__ does not compare children, so check them explicitly
        assert len(promptex_loaded.elements[i].elements) == len(promptex_original.elements[i].elements)
        if promptex_original.elements[i].elements:
            for j in range(len(promptex_original.elements[i].elements)):
                 assert promptex_loaded.elements[i].elements[j] == promptex_original.elements[i].elements[j]


def test_promptex_get_prompt_no_elements():
    promptex = Promptex()
    strategy = SimpleTextEncodingStrategy()
    # The behavior was changed in Promptex.get_prompt to return "" and log a warning if no elements
    # Previous expectation: pytest.raises(ValueError, match="No elements to encode")
    assert promptex.get_prompt(strategy) == ""


def test_promptex_get_prompt_with_strategy(role, instruction):
    promptex = Promptex()
    promptex.add_elements([role, instruction]) # role fixture is Role("Role"), instruction is Instruction("Instruction")

    # Test with MagicMock
    mock_strategy = MagicMock(spec=BaseEncodingStrategy)
    mock_strategy.encode.return_value = "mocked_prompt"
    result = promptex.get_prompt(mock_strategy)
    mock_strategy.encode.assert_called_once_with(promptex)
    assert result == "mocked_prompt"

    # Test with actual SimpleTextEncodingStrategy (default params)
    # Elements are added in order: Role("Role"), Instruction("Instruction")
    # Default SimpleTextEncodingStrategy: separator="\n\n", delimiter="---", prefix_delimiter=True
    # Output for Role("Role"): "--- ROLE ---\nRole\n"
    # Output for Instruction("Instruction"): "--- INSTRUCTION ---\nInstruction\n"
    # Joined by "\n\n"
    strategy_actual = SimpleTextEncodingStrategy()
    expected_output = (
        "--- ROLE ---\nRole\n"
        "\n\n"
        "--- INSTRUCTION ---\nInstruction\n"
    )
    actual_output = promptex.get_prompt(strategy_actual)
    assert actual_output == expected_output

def test_promptex_get_token_count():
    promptex = Promptex() # Not strictly needed to be a Promptex method if it's static like
    text1 = "Hello world" # 2 tokens with gpt-4
    count1 = promptex.get_token_count(text1, encoding_model_name="gpt-4")
    assert count1 == 2

    text2 = "こんにちは世界" # Japanese text
    # Exact token count can vary, but should be positive and typically more than 1 per char for CJK
    # For "こんにちは世界" (7 chars), it's likely around 7-9 tokens.
    # "こんにちは世界" -> ['こ', 'ん', 'にちは', '世界'] -> 4 tokens by cl100k_base/gpt-4
    count2 = promptex.get_token_count(text2, encoding_model_name="gpt-4")
    assert count2 == 4 # Adjusted based on tiktoken behavior for this string

def test_promptex_str_representation(role):
    promptex = Promptex()
    promptex.add_elements([role]) # Role("Role")

    # Default SimpleTextEncodingStrategy output for Role("Role"):
    # "--- ROLE ---\nRole\n"
    text_strategy_output = promptex.get_prompt(SimpleTextEncodingStrategy())
    assert str(promptex) == text_strategy_output
    assert str(promptex) == "--- ROLE ---\nRole\n"


def test_promptex_get_stats_no_elements():
    promptex = Promptex()
    stats = promptex.get_stats(encoding_model_name="gpt-4")
    assert stats["element_count"] == {"total": 0}
    assert stats["text_length"] == {"total": 0} # text_length only has 'total' if no elements
    assert stats["token_count"] == {"total": 0} # token_count only has 'total' if no elements

def test_promptex_get_stats_with_elements():
    promptex = Promptex()
    r = Role("User")  # text len 4, tokens 1 ("User")
    i = Instruction("Test this thoroughly.") # text len 20, tokens 4 ("Test", " this", " thoroughly", ".")
    c_empty = Context("") # text len 0, tokens 0

    promptex.add_elements([r, i, c_empty])
    stats = promptex.get_stats(encoding_model_name="gpt-4")

    assert stats["element_count"]["total"] == 3
    assert stats["element_count"]["role"] == 1 # Element types are lowercase strings
    assert stats["element_count"]["instruction"] == 1
    assert stats["element_count"]["context"] == 1

    # Text length stats for 'role' type
    assert stats["text_length"]["role"]["min"] == 4
    assert stats["text_length"]["role"]["max"] == 4
    assert stats["text_length"]["role"]["avg"] == 4.0

    # Token count stats for 'role' type
    assert stats["token_count"]["role"]["min"] == 1
    assert stats["token_count"]["role"]["max"] == 1
    assert stats["token_count"]["role"]["avg"] == 1.0

    # Text length stats for 'instruction' type
    assert stats["text_length"]["instruction"]["min"] == 20
    assert stats["text_length"]["instruction"]["max"] == 20
    assert stats["text_length"]["instruction"]["avg"] == 20.0

    # Token count stats for 'instruction' type
    assert stats["token_count"]["instruction"]["min"] == 4
    assert stats["token_count"]["instruction"]["max"] == 4
    assert stats["token_count"]["instruction"]["avg"] == 4.0

    # Text length stats for 'context' type
    assert stats["text_length"]["context"]["min"] == 0
    assert stats["text_length"]["context"]["max"] == 0
    assert stats["text_length"]["context"]["avg"] == 0.0

    # Token count stats for 'context' type
    assert stats["token_count"]["context"]["min"] == 0
    assert stats["token_count"]["context"]["max"] == 0
    assert stats["token_count"]["context"]["avg"] == 0.0

    # Total text length:
    # r_text = "--- ROLE ---\nUser\n" (len 18)
    # i_text = "--- INSTRUCTION ---\nTest this thoroughly.\n" (len 45)
    # c_text = "--- CONTEXT ---\n\n" (len 17)
    # separator = "\n\n" (len 2)
    # Total = 18 + 2 + 45 + 2 + 17 = 84
    assert stats["text_length"]["total"] == 84

    # Total token count for "--- ROLE ---\nUser\n\n\n--- INSTRUCTION ---\nTest this thoroughly.\n\n\n--- CONTEXT ---\n\n"
    # This is complex to calculate by hand exactly.
    # "--- ROLE ---\nUser\n" -> "---", " ROLE", " ---", "\n", "User", "\n" -> 6 if split, but tiktoken is different
    # Let's verify it's the sum of parts plus separators' tokens if possible, or just greater than sum of individual text tokens.
    # "User" -> 1, "Test this thoroughly." -> 4, "" -> 0. Sum = 5.
    # The full string "--- ROLE ---\nUser\n\n\n--- INSTRUCTION ---\nTest this thoroughly.\n\n\n--- CONTEXT ---\n\n"
    # when tokenized with gpt-4 model gives:
    # ['---', ' ROLE', ' ---', '\n', 'User', '\n\n\n', '---', ' INSTRUCTION', ' ---', '\n', 'Test', ' this', ' thoroughly', '.', '\n\n\n', '---', ' CONTEXT', ' ---', '\n\n']
    # This is 19 tokens.
    assert stats["token_count"]["total"] == 19
