from pyramid import testing
import pytest
"""conftest path throwing errors.  these files moved here per Scott"""


@pytest.fixture
def dummy_request():
    return testing.DummyRequest()


@pytest.fixture
def dummy_auth_request():
    request = testing.DummyRequest(method='POST', params={'username': 'dummy', 'email': 'wat@wat.com', 'password': 'pass'})

    return request


"""tests below, conftest above"""
from pyramid_stocks.views.default import register_view
from pyramid.httpexceptions import HTTPFound


def test_signin_to_auth_view(dummy_request):
    request = dummy_request
    request.method = 'GET'
    # import pbd ; pbd.set_trace()

    response = register_view(dummy_request)

    assert isinstance(response, HTTPFound)
    assert response.status_code == 302