import pytest
from storm.core.application import StormApplication
from storm.common.decorators import Module

@Module()
class TestModule:
    initialized = False
    destroyed = False

    def onInit(self):
        self.initialized = True

    def onDestroy(self):
        self.destroyed = True

@pytest.mark.asyncio
async def test_module_initialization():
    app = StormApplication(root_module=TestModule)
    assert TestModule.initialized == True

@pytest.mark.asyncio
async def test_module_shutdown():
    app = StormApplication(root_module=TestModule)
    app.shutdown()
    assert TestModule.destroyed == True
