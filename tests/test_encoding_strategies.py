import pytest
from promptex import Promptex
from promptex.elements import Element, Role, Instruction, Context, Constraint, InputData, OutputFormat
from promptex.elements.element_type import ElementType
from promptex.encoding_strategy import (
    SimpleTextEncodingStrategy,
    SimpleCsvEncodingStrategy,
    SimpleHtmlEncodingStrategy,
    SimpleJsonEncodingStrategy,
    SimpleJsonSchemaEncodingStrategy,
    SimpleMarkdownEncodingStrategy,
    SimpleXmlEncodingStrategy,
    SimpleYamlEncodingStrategy,
)
import xml.etree.ElementTree as ET # For XML strategy
from xml.dom.minidom import parseString # For XML pretty printing
import json # For JSON strategy
import yaml # For YAML strategy
import csv # For CSV strategy
import io # For CSV strategy
import os # For CSV test platform-specific newline
import warnings # For XML strategy warning test

# Fixtures for common elements
@pytest.fixture
def role_el():
    return Role("Test Role") # type="role", default priority=1

@pytest.fixture
def instruction_el():
    return Instruction("Test Instruction") # type="instruction", default priority=2

@pytest.fixture
def context_el():
    return Context("Test Context") # type="context", default priority=4

@pytest.fixture
def constraint_el():
    return Constraint("Test Constraint") # type="constraint", default priority=3

# --- Tests for SimpleTextEncodingStrategy ---

@pytest.fixture
def text_strategy():
    return SimpleTextEncodingStrategy()

@pytest.fixture
def text_strategy_custom():
    return SimpleTextEncodingStrategy(separator="|", delimiter="*", prefix_delimiter=False)

def test_text_empty(text_strategy):
    promptex = Promptex()
    assert text_strategy.encode(promptex) == ""

def test_text_single_element(text_strategy, role_el):
    promptex = Promptex()
    promptex.add_elements([role_el])
    assert text_strategy.encode(promptex) == "--- ROLE ---\nTest Role\n"

def test_text_multiple_elements(text_strategy, role_el, instruction_el):
    promptex = Promptex()
    promptex.add_elements([role_el, instruction_el])
    expected = (
        "--- ROLE ---\nTest Role\n"
        "\n\n"
        "--- INSTRUCTION ---\nTest Instruction\n"
    )
    assert text_strategy.encode(promptex) == expected

def test_text_nested_elements(text_strategy):
    promptex = Promptex()
    parent = Instruction("Main Task Parent")

    child_high_prio = Context("C_HIGH: Context with higher priority val")
    child_high_prio.priority = 10

    child_low_prio = Constraint("C_LOW: Constraint with lower priority val")
    child_low_prio.priority = 5

    parent.add_elements([child_low_prio, child_high_prio])
    promptex.add_elements([parent])

    expected = (
        "--- INSTRUCTION ---\nMain Task Parent\n"
        "\n\n"
        "--- CONTEXT ---\nC_HIGH: Context with higher priority val\n"
        "\n\n"
        "--- CONSTRAINT ---\nC_LOW: Constraint with lower priority val\n"
    )
    result = text_strategy.encode(promptex)
    assert result == expected
    assert result.find("C_HIGH: Context with higher priority val") < result.find("C_LOW: Constraint with lower priority val")

def test_text_custom_params(text_strategy_custom):
    promptex = Promptex()
    promptex.add_elements([Role("Test Role"), Instruction("Test Instruction")])
    expected = (
        "ROLE\nTest Role\n"
        "|"
        "INSTRUCTION\nTest Instruction\n"
    )
    assert text_strategy_custom.encode(promptex) == expected

# --- Tests for SimpleCsvEncodingStrategy ---

@pytest.fixture
def csv_strategy():
    return SimpleCsvEncodingStrategy()

def test_csv_empty(csv_strategy):
    promptex = Promptex()
    assert csv_strategy.encode(promptex) == ""

def test_csv_single_element(csv_strategy, role_el):
    promptex = Promptex()
    promptex.add_elements([role_el])
    output = csv_strategy.encode(promptex)
    reader = csv.reader(io.StringIO(output))
    rows = list(reader)
    assert len(rows) == 1
    assert rows[0] == ["ROLE", "Test Role"]

def test_csv_multiple_elements(csv_strategy, role_el, instruction_el):
    promptex = Promptex()
    promptex.add_elements([role_el, instruction_el])
    output = csv_strategy.encode(promptex)
    reader = csv.reader(io.StringIO(output))
    rows = list(reader)
    assert len(rows) == 2
    assert rows[0] == ["ROLE", "Test Role"]
    assert rows[1] == ["INSTRUCTION", "Test Instruction"]

def test_csv_nested_elements(csv_strategy):
    promptex = Promptex()
    parent = Instruction("Main Task Parent")

    child_high_prio = Context("C_HIGH Context")
    child_high_prio.priority = 10 # This priority will be used for sorting children
    child_low_prio = Constraint("C_LOW Constraint")
    child_low_prio.priority = 5   # This priority will be used for sorting children

    # Add in order: low prio, then high prio. Expect high prio first in output due to get_sorted_children.
    parent.add_elements([child_low_prio, child_high_prio])
    promptex.add_elements([parent])

    output = csv_strategy.encode(promptex)
    reader = csv.reader(io.StringIO(output))
    rows = list(reader)
    assert len(rows) == 1
    expected_row_data = [
        "INSTRUCTION", "Main Task Parent",
        "CONTEXT", "C_HIGH Context",       # Child high prio (sorted first)
        "CONSTRAINT", "C_LOW Constraint"    # Child low prio (sorted second)
    ]
    assert rows[0] == expected_row_data

# --- Tests for SimpleHtmlEncodingStrategy ---

@pytest.fixture
def html_strategy():
    return SimpleHtmlEncodingStrategy()

def test_html_empty(html_strategy):
    promptex = Promptex()
    assert html_strategy.encode(promptex) == ""

def test_html_single_element(html_strategy, role_el):
    promptex = Promptex()
    promptex.add_elements([role_el])
    result = html_strategy.encode(promptex)
    expected_content = "<h2>Test Role\n</h2>"
    assert expected_content in result
    assert result.startswith("<html>")
    assert result.endswith("</html>")

def test_html_multiple_elements(html_strategy, role_el, instruction_el):
    promptex = Promptex()
    promptex.add_elements([role_el, instruction_el])
    result = html_strategy.encode(promptex)
    role_content = "<h2>Test Role\n</h2>"
    inst_content = "<h1>Test Instruction\n</h1>"
    assert role_content in result
    assert inst_content in result
    assert result.find(role_content) < result.find(inst_content) # Order preserved

def test_html_nested_elements(html_strategy):
    promptex = Promptex()
    parent = Instruction("Parent Inst")

    child_high_prio = Context("High Prio Ctx")
    child_high_prio.priority = 10
    child_low_prio = Constraint("Low Prio Con")
    child_low_prio.priority = 5

    parent.add_elements([child_low_prio, child_high_prio]) # low then high
    promptex.add_elements([parent])

    result = html_strategy.encode(promptex)
    high_prio_content = "<p>High Prio Ctx\n</p>" # Context is <p>
    low_prio_content = "<h3>Low Prio Con\n</h3>" # Constraint is <h3>

    assert high_prio_content in result
    assert low_prio_content in result
    assert result.find(high_prio_content) < result.find(low_prio_content) # High prio child first

    expected_parent_open = "<h1>Parent Inst"
    expected_parent_close = "</h1>"
    assert expected_parent_open in result
    assert expected_parent_close in result
    parent_open_idx = result.find(expected_parent_open)
    parent_close_idx = result.rfind(expected_parent_close)
    assert parent_open_idx != -1 and parent_close_idx != -1 and parent_open_idx < parent_close_idx

    child_high_idx = result.find(high_prio_content)
    child_low_idx = result.find(low_prio_content)
    assert parent_open_idx < child_high_idx < parent_close_idx
    assert parent_open_idx < child_low_idx < parent_close_idx

def test_html_text_sanitization(html_strategy):
    promptex = Promptex()
    # Default tag for unknown "test" type is <p>
    el = Element("test", "Text with < & > characters", priority=1)
    promptex.add_elements([el])
    result = html_strategy.encode(promptex)
    expected_content_actual = "<p>Text with &lt; & &gt; characters\n</p>"
    assert expected_content_actual in result

# --- Tests for SimpleJsonEncodingStrategy ---

@pytest.fixture
def json_strategy():
    return SimpleJsonEncodingStrategy()

def test_json_empty(json_strategy):
    promptex = Promptex()
    assert json.loads(json_strategy.encode(promptex)) == []

def test_json_single_element(json_strategy, role_el):
    promptex = Promptex()
    role_el.priority = 7
    promptex.add_elements([role_el])
    result = json.loads(json_strategy.encode(promptex))
    assert len(result) == 1
    expected_el_dict = {
        "type": "role",
        "text": "Test Role",
        "priority": 7 # Priority included
    }
    assert result[0] == expected_el_dict

def test_json_multiple_elements(json_strategy, role_el, instruction_el):
    promptex = Promptex()
    # Order of elements in promptex.elements is preserved
    promptex.add_elements([role_el, instruction_el])
    result = json.loads(json_strategy.encode(promptex))
    assert len(result) == 2
    assert result[0]["type"] == "role"
    assert result[0]["text"] == "Test Role"
    assert result[0]["priority"] == ElementType.ROLE.priority
    assert result[1]["type"] == "instruction"
    assert result[1]["text"] == "Test Instruction"
    assert result[1]["priority"] == ElementType.INSTRUCTION.priority

def test_json_nested_elements(json_strategy):
    promptex = Promptex()
    parent = Instruction("Main Task Parent")
    parent.priority = 15 # Parent's priority

    child_high_prio = Context("C_HIGH Context")
    child_high_prio.priority = 10 # Child's explicit priority
    child_low_prio = Constraint("C_LOW Constraint")
    child_low_prio.priority = 5   # Child's explicit priority

    # Add low prio child, then high prio child to parent
    parent.add_elements([child_low_prio, child_high_prio])
    promptex.add_elements([parent]) # Add parent to promptex

    result = json.loads(json_strategy.encode(promptex))
    assert len(result) == 1 # Only one top-level element (parent)
    parent_dict = result[0]
    assert parent_dict["type"] == "instruction"
    assert parent_dict["text"] == "Main Task Parent"
    assert parent_dict["priority"] == 15
    assert "children" in parent_dict # Key for children list

    children_list = parent_dict["children"]
    assert len(children_list) == 2

    # Children are sorted by priority (descending): high_prio (10), then low_prio (5)
    assert children_list[0]["type"] == "context"
    assert children_list[0]["text"] == "C_HIGH Context"
    assert children_list[0]["priority"] == 10 # Children's priorities are in their dicts

    assert children_list[1]["type"] == "constraint"
    assert children_list[1]["text"] == "C_LOW Constraint"
    assert children_list[1]["priority"] == 5

# --- Tests for SimpleMarkdownEncodingStrategy ---

@pytest.fixture
def md_strategy():
    return SimpleMarkdownEncodingStrategy()

def test_md_empty(md_strategy):
    promptex = Promptex()
    assert md_strategy.encode(promptex) == ""

def test_md_single_element(md_strategy, role_el):
    promptex = Promptex()
    promptex.add_elements([role_el])
    # Default _encode_element: f"{'#' * depth} {element.type.capitalize()}\n{element.text}\n\n"
    # element.type for Role("Test Role") is "role". Capitalized: "Role"
    expected = "# Role\nTest Role\n\n"
    assert md_strategy.encode(promptex) == expected

def test_md_multiple_elements(md_strategy, role_el, instruction_el):
    promptex = Promptex()
    promptex.add_elements([role_el, instruction_el]) # Order preserved
    expected = (
        "# Role\nTest Role\n\n"                 # First element
        "# Instruction\nTest Instruction\n\n"  # Second element, no separator by default
    )
    assert md_strategy.encode(promptex) == expected

def test_md_nested_elements(md_strategy):
    promptex = Promptex()
    parent = Instruction("Main Task: Parent") # Depth 1

    child_high_prio = Context("CTX_H: High Prio") # Depth 2
    child_high_prio.priority = 10
    child_low_prio = Constraint("CON_L: Low Prio") # Depth 2
    child_low_prio.priority = 5

    parent.add_elements([child_low_prio, child_high_prio]) # low then high
    promptex.add_elements([parent])

    expected = (
        "# Instruction\nMain Task: Parent\n\n"  # Parent
        "## Context\nCTX_H: High Prio\n\n"      # Child high (sorted first)
        "## Constraint\nCON_L: Low Prio\n\n"   # Child low (sorted second)
    )
    result = md_strategy.encode(promptex)
    assert result == expected
    assert result.find("CTX_H: High Prio") < result.find("CON_L: Low Prio")

def test_md_heading_depth_limit(md_strategy):
    promptex = Promptex()
    # Element types are capitalized by this strategy.
    el = Element("Level1", "text1") # type "Level1"
    child1 = Element("Level2", "text2")
    child2 = Element("Level3", "text3")
    child3 = Element("Level4", "text4")
    child4 = Element("Level5", "text5")
    child5 = Element("Level6", "text6")
    child6 = Element("Level7", "text7") # Should be capped at ###### (depth 6)

    child5.add_element(child6)
    child4.add_element(child5)
    child3.add_element(child4)
    child2.add_element(child3)
    child1.add_element(child2)
    el.add_element(child1)
    promptex.add_elements([el])

    result = md_strategy.encode(promptex)
    # Check type capitalization from strategy
    assert "# Level1\ntext1\n\n" in result
    assert "## Level2\ntext2\n\n" in result
    assert "### Level3\ntext3\n\n" in result
    assert "#### Level4\ntext4\n\n" in result
    assert "##### Level5\ntext5\n\n" in result
    assert "###### Level6\ntext6\n\n" in result
    assert "###### Level7\ntext7\n\n" in result # Capped at depth 6, type "Level7"

# --- Tests for SimpleXmlEncodingStrategy ---

@pytest.fixture
def xml_strategy():
    return SimpleXmlEncodingStrategy()

def test_xml_empty(xml_strategy):
    promptex = Promptex()
    assert xml_strategy.encode(promptex) == ""

def test_xml_single_element(xml_strategy, role_el):
    promptex = Promptex()
    role_el.priority = 7 # Non-default to test attribute
    promptex.add_elements([role_el]) # type "role"
    result_str = xml_strategy.encode(promptex)

    root = ET.fromstring(result_str) # Main root is <promptex>
    assert root.tag == "promptex"
    assert len(list(root)) == 1 # One child element under <promptex>
    xml_el = root[0]
    assert xml_el.tag == "role" # Element.type is used directly for tag
    assert xml_el.text == "Test Role"
    assert xml_el.get("priority") == "7" # Priority as attribute

def test_xml_multiple_elements(xml_strategy, role_el, instruction_el):
    promptex = Promptex()
    promptex.add_elements([role_el, instruction_el]) # Order preserved
    result_str = xml_strategy.encode(promptex)

    root = ET.fromstring(result_str)
    assert root.tag == "promptex"
    assert len(list(root)) == 2 # Two child elements

    assert list(root)[0].tag == "role"
    assert list(root)[0].text == "Test Role"
    assert list(root)[0].get("priority") == str(ElementType.ROLE.priority) # Default priority

    assert list(root)[1].tag == "instruction"
    assert list(root)[1].text == "Test Instruction"
    assert list(root)[1].get("priority") == str(ElementType.INSTRUCTION.priority) # Default


def test_xml_nested_elements(xml_strategy):
    promptex = Promptex()
    parent = Instruction("Main Task Parent")
    parent.priority = 15 # Parent's explicit priority

    child_high_prio = Context("C_HIGH Context")
    child_high_prio.priority = 10 # Child's explicit priority
    child_low_prio = Constraint("C_LOW Constraint")
    child_low_prio.priority = 5   # Child's explicit priority

    parent.add_elements([child_low_prio, child_high_prio]) # Add low, then high
    promptex.add_elements([parent])

    result_str = xml_strategy.encode(promptex)
    root = ET.fromstring(result_str)
    assert len(list(root)) == 1 # One top-level element
    parent_xml = root[0]
    assert parent_xml.tag == "instruction"
    assert parent_xml.text == "Main Task Parent"
    assert parent_xml.get("priority") == "15"

    children_xml = list(parent_xml) # Children of <instruction>
    assert len(children_xml) == 2

    # Children sorted by priority (desc): high_prio (10), then low_prio (5)
    assert children_xml[0].tag == "context"
    assert children_xml[0].text == "C_HIGH Context"
    assert children_xml[0].get("priority") == "10"

    assert children_xml[1].tag == "constraint"
    assert children_xml[1].text == "C_LOW Constraint"
    assert children_xml[1].get("priority") == "5"

def test_xml_tag_name_sanitization_and_warning(xml_strategy):
    promptex = Promptex()
    el = Element("invalid tag name with spaces:and:colons", "test text", priority=1)
    promptex.add_elements([el])

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result_str = xml_strategy.encode(promptex)

        assert len(w) >= 1
        assert any("Invalid XML tag name" in str(warn_msg.message) for warn_msg in w)

    root = ET.fromstring(result_str)
    xml_el = root[0] # The <element original_type="...">
    assert xml_el.tag == "element" # Default tag for invalid names
    assert xml_el.get("original_type") == "invalid tag name with spaces:and:colons"
    assert xml_el.text == "test text"

# --- Tests for SimpleYamlEncodingStrategy ---

@pytest.fixture
def yaml_strategy():
    return SimpleYamlEncodingStrategy()

def test_yaml_empty(yaml_strategy):
    promptex = Promptex()
    result = yaml_strategy.encode(promptex)
    assert yaml.safe_load(result) == [] # Expect empty list

def test_yaml_single_element(yaml_strategy, role_el):
    promptex = Promptex()
    # role_el priority is ElementType.ROLE.priority (1), not used in structure
    promptex.add_elements([role_el])
    result = yaml.safe_load(yaml_strategy.encode(promptex))

    assert len(result) == 1
    expected_el_dict = {
        "role": { # Type is the key
            "text": "Test Role"
            # No "children" if none, no priority by default in this strategy's output
        }
    }
    assert result[0] == expected_el_dict

def test_yaml_multiple_elements(yaml_strategy, role_el, instruction_el):
    promptex = Promptex()
    promptex.add_elements([role_el, instruction_el]) # Order preserved
    result = yaml.safe_load(yaml_strategy.encode(promptex))
    assert len(result) == 2
    assert result[0] == {"role": {"text": "Test Role"}}
    assert result[1] == {"instruction": {"text": "Test Instruction"}}

def test_yaml_nested_elements(yaml_strategy):
    promptex = Promptex()
    parent = Instruction("Main Task Parent")
    # Parent's priority is not directly in YAML output structure by this strategy

    child_high_prio = Context("C_HIGH Context")
    child_high_prio.priority = 10 # Child's explicit priority
    child_low_prio = Constraint("C_LOW Constraint")
    child_low_prio.priority = 5   # Child's explicit priority

    parent.add_elements([child_low_prio, child_high_prio]) # Add low, then high
    promptex.add_elements([parent])

    result = yaml.safe_load(yaml_strategy.encode(promptex))
    assert len(result) == 1 # One top-level element (parent)
    parent_yaml_obj = result[0] # This is a dict like {"instruction": {...content...}}
    assert "instruction" in parent_yaml_obj
    parent_content = parent_yaml_obj["instruction"]
    assert parent_content["text"] == "Main Task Parent"
    assert "children" in parent_content # Key for children list

    children_list = parent_content["children"]
    assert len(children_list) == 2

    # Children sorted by priority (desc): high_prio (10), then low_prio (5)
    assert children_list[0] == {"context": {"text": "C_HIGH Context"}}
    assert children_list[1] == {"constraint": {"text": "C_LOW Constraint"}}


# --- Tests for SimpleJsonSchemaEncodingStrategy ---

@pytest.fixture
def schema_strategy():
    return SimpleJsonSchemaEncodingStrategy()

def test_schema_empty(schema_strategy):
    promptex = Promptex()
    result = json.loads(schema_strategy.encode(promptex))
    expected_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {},
    }
    assert result == expected_schema

def test_schema_single_element_no_children(schema_strategy, role_el):
    promptex = Promptex()
    promptex.add_elements([role_el]) # Role("Test Role")
    result = json.loads(schema_strategy.encode(promptex))

    assert result["properties"]["role"]["type"] == "object"
    assert result["properties"]["role"]["title"] == "Element: role"
    assert "text" in result["properties"]["role"]["properties"]
    assert result["properties"]["role"]["properties"]["text"]["type"] == "string"
    assert "children" not in result["properties"]["role"]["properties"] # No children
    assert result["required"] == ["role"]

def test_schema_multiple_elements_no_children(schema_strategy, role_el, instruction_el):
    promptex = Promptex()
    promptex.add_elements([role_el, instruction_el]) # Order is preserved in properties
    result = json.loads(schema_strategy.encode(promptex))

    assert list(result["properties"].keys()) == ["role", "instruction"]
    assert result["required"] == ["role", "instruction"]
    assert "text" in result["properties"]["instruction"]["properties"]

def test_schema_nested_elements_order_preserved(schema_strategy):
    # JSON Schema strategy does NOT sort children by priority. Order is from element.elements.
    promptex = Promptex()
    parent = Instruction("Parent Task")

    # Add children in a specific order, priorities are ignored for schema structure.
    child1_ctx = Context("Child Context - First")
    child1_ctx.priority = 10 # High priority, but added first
    child2_con = Constraint("Child Constraint - Second")
    child2_con.priority = 5 # Low priority, but added second

    parent.add_elements([child1_ctx, child2_con]) # Order: Context, then Constraint
    promptex.add_elements([parent])

    result = json.loads(schema_strategy.encode(promptex))

    parent_schema = result["properties"]["instruction"]
    assert "children" in parent_schema["properties"]
    children_prop_schema = parent_schema["properties"]["children"]
    assert children_prop_schema["type"] == "array"

    # Check items - this is where the structure of children is defined
    # The refactored strategy uses oneOf if multiple children, or direct schema if one child.
    items_schema = children_prop_schema["items"]
    assert "oneOf" in items_schema
    assert len(items_schema["oneOf"]) == 2 # Two distinct child element schemas

    # The order in "oneOf" should reflect the order in parent.elements
    # First child added was Context
    assert items_schema["oneOf"][0]["title"] == "Element: context"
    assert "text" in items_schema["oneOf"][0]["properties"]
    assert items_schema["oneOf"][0]["properties"]["text"]["type"] == "string"
    # Second child added was Constraint
    assert items_schema["oneOf"][1]["title"] == "Element: constraint"
    assert "text" in items_schema["oneOf"][1]["properties"]
    assert items_schema["oneOf"][1]["properties"]["text"]["type"] == "string"

def test_schema_element_with_no_text(schema_strategy):
    promptex = Promptex()
    el_no_text = Element(type="test_type", text="") # Empty text
    promptex.add_elements([el_no_text])
    result = json.loads(schema_strategy.encode(promptex))
    # "text" property should not be required, or might be absent from properties if text is empty.
    # Current impl: if element.text is an empty string, it's still added.
    # And it's in "required" array. This might be desired or not.
    # Let's assume current behavior is intended.
    assert "text" in result["properties"]["test_type"]["properties"]
    assert "text" in result["properties"]["test_type"]["required"]

    el_no_text_at_all = Element(type="another", text=None) # text is None
    promptex.set_elements([el_no_text_at_all]) # Replace elements
    result2 = json.loads(schema_strategy.encode(promptex))
    # If text is None, it's not added to properties by `if element.text:`
    assert "text" not in result2["properties"]["another"]["properties"]
    assert "text" not in (result2["properties"]["another"].get("required") or [])

def test_schema_element_with_child_having_no_text(schema_strategy):
    promptex = Promptex()
    parent = Instruction("Parent")
    child_no_text = Context("") # Child with empty text
    parent.add_element(child_no_text)
    promptex.add_elements([parent])

    result = json.loads(schema_strategy.encode(promptex))
    parent_schema = result["properties"]["instruction"]
    child_item_schema = parent_schema["properties"]["children"]["items"] # single child, so items is the schema itself

    assert child_item_schema["title"] == "Element: context"
    assert "text" in child_item_schema["properties"] # text property is defined
    assert "text" in child_item_schema["required"]   # and required
