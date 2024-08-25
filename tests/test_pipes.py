import pytest
import asyncio
from storm.common.pipes.validate_non_empty_pipe import ValidateNonEmptyPipe
from storm.common.pipes.to_uppercase_pipe import ToUpperCasePipe

@pytest.mark.asyncio
async def test_validate_non_empty_pipe():
    pipe = ValidateNonEmptyPipe()

    # Test with a valid non-empty string
    valid_input = "Valid String"
    result = await pipe.transform(valid_input)
    assert result == valid_input

    # Test with an empty string
    with pytest.raises(ValueError, match="Value must be a non-empty string"):
        await pipe.transform("")

    # Test with a non-string value
    with pytest.raises(ValueError, match="Value must be a non-empty string"):
        await pipe.transform(123)

@pytest.mark.asyncio
async def test_to_uppercase_pipe():
    pipe = ToUpperCasePipe()

    # Test with a valid string
    input_value = "hello"
    expected_output = "HELLO"
    result = await pipe.transform(input_value)
    assert result == expected_output

    # Test with a string that's already uppercase
    input_value = "WORLD"
    expected_output = "WORLD"
    result = await pipe.transform(input_value)
    assert result == expected_output

    # Test with a non-string value (should return the value unchanged)
    input_value = 123
    result = await pipe.transform(input_value)
    assert result == input_value
