# tests/common/decorators/http/test_render.py

from storm.common.constants import RENDER_METADATA
from storm.common.decorators.http.render import Render
from storm.core.di.reflect import Reflect


def test_render_sets_template_metadata():
    class Controller:
        @Render("index.html")
        def handler(self):
            pass

    template = Reflect.get_metadata(RENDER_METADATA, Controller.handler)
    assert template == "index.html"
