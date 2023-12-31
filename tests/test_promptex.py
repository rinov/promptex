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
