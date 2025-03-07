"""Test utils."""
from typing import List

from pydantic import Field

from llama_index.tools.utils import create_schema_from_function


def test_create_schema_from_function() -> None:
    """Test create schema from function."""

    def test_fn(x: int, y: int, z: List[str]) -> None:
        """Test function."""
        pass

    SchemaCls = create_schema_from_function("test_schema", test_fn)
    schema = SchemaCls.schema()
    assert schema["properties"]["x"]["type"] == "integer"
    assert schema["properties"]["y"]["type"] == "integer"
    assert schema["properties"]["z"]["type"] == "array"
    assert schema["required"] == ["x", "y", "z"]

    SchemaCls = create_schema_from_function("test_schema", test_fn, [("a", bool, 1)])
    schema = SchemaCls.schema()
    assert schema["properties"]["a"]["type"] == "boolean"

    def test_fn2(x: int = 1) -> None:
        """Optional input"""
        pass

    SchemaCls = create_schema_from_function("test_schema", test_fn2)
    schema = SchemaCls.schema()
    assert "required" not in schema


def test_create_schema_from_function_with_field() -> None:
    """Test create_schema_from_function with pydantic.Field."""

    def tmp_function(x: int = Field(3, description="An integer")) -> str:
        return str(x)

    schema = create_schema_from_function("TestSchema", tmp_function)
    actual_schema = schema.schema()

    assert "x" in actual_schema["properties"]
    assert actual_schema["properties"]["x"]["type"] == "integer"
    assert actual_schema["properties"]["x"]["default"] == 3
    assert actual_schema["properties"]["x"]["description"] == "An integer"

    # Test the created schema
    instance = schema()
    assert instance.x == 3  # type: ignore

    instance = schema(x=5)
    assert instance.x == 5  # type: ignore
