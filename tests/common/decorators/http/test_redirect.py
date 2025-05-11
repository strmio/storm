# tests/common/decorators/http/test_redirect.py

from storm.common.constants import REDIRECT_METADATA
from storm.common.decorators.http.redirect import Redirect
from storm.core.di.reflect import Reflect


def test_redirect_sets_url_and_status():
    @Redirect("/new-location", 301)
    def redirect_view():
        pass

    metadata = Reflect.get_metadata(REDIRECT_METADATA, redirect_view)
    assert metadata == {"url": "/new-location", "statusCode": 301}


def test_redirect_defaults_to_empty_url_and_none_status():
    @Redirect()
    def default_redirect():
        pass

    metadata = Reflect.get_metadata(REDIRECT_METADATA, default_redirect)
    assert metadata == {"url": "", "statusCode": None}
