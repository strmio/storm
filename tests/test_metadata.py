from storm.common.decorators import add_metadata, get_metadata

def test_add_metadata():
    @add_metadata('role', 'admin')
    async def handler():
        return "Handled"

    assert get_metadata(handler, 'role') == 'admin'
