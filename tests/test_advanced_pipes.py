import pytest
from storm.common.pipes.json_to_dict_pipe import JsonToDictPipe
from storm.common.pipes.email_validation_pipe import EmailValidationPipe

@pytest.mark.asyncio
async def test_json_to_dict_pipe():
    pipe = JsonToDictPipe()

    json_input = '{"key": "value"}'
    result = await pipe.transform(json_input)
    assert result == {"key": "value"}

    with pytest.raises(ValueError, match="Invalid JSON format"):
        await pipe.transform("{key: value}")

@pytest.mark.asyncio
async def test_email_validation_pipe():
    pipe = EmailValidationPipe()

    valid_email = "test@example.com"
    result = await pipe.transform(valid_email)
    assert result == valid_email

    with pytest.raises(ValueError, match="Invalid email address"):
        await pipe.transform("invalid-email")
