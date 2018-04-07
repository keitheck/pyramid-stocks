def test_signin_to_auth_view(dummy_auth_request):
    from ..views.default import register_view
    from pyramid.httpexceptions import HTTPFound
    request = dummy_auth_request
    request.method = 'GET'
    # import pbd ; pbd.set_trace()
    assert isinstance(response, HTTPFound)
    assert response.status_code is 302