import pytest
from pyramid import testing
from ..models.meta import Base
from ..models import My_stocks

"""conftest moved here per Scott to try to get tests to run"""

@pytest.fixture
def configuration(request):
    """add db for tests"""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/pyramid_test'
    })

    config.include('pyramid_stocks.models')
    config.include('pyramid_stocks.routes')
    
    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """this is a test database session to communicate with the test database."""
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Create a dummy GET request with a dbsession."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def test_entry():
    """test stock for testing database entry"""
    return My_stocks(
        id=1,
        symbol='ABC',
        companyName='ABC co',
        exchange='XYse',
        industry='industry',
        CEO='CEO',
        description='description',
        sector='sector',
        issueType='issueType',
        website='website',
    )


"""end fixtures"""


def test_if_true():
    """test pytest is working"""
    assert True is True


def test_index_view(dummy_request):
    """test home"""
    from ..views.default import home_view
    assert home_view(dummy_request) == {}


def test_index_view_ii(dummy_request):
    """test home response type"""
    from ..views.default import home_view
    response = home_view(dummy_request)
    assert type(response) == dict  


def test_index_view_iii(dummy_request):
    """test home response type"""
    from ..views.default import home_view
    response = home_view(dummy_request)
    assert len(response) == 0  


def test_auth_view_resopnse(dummy_request):
    """test portfolio response is dict"""
    from ..views.auth import register_view
    assert register_view(dummy_request) == {}
     

def test_auth_signin_view(dummy_request):
    """test response status code signin"""
    from ..views.auth import register_view

    dummy_request.GET = {'username': 'joe', 'password': '1234'}
    response = register_view(dummy_request)
    assert response.status_code == 401 


def test_auth_signin_view_instance(dummy_request):
    """test unathorized signin"""
    from ..views.auth import register_view
    from pyramid.httpexceptions import HTTPUnauthorized

    dummy_request.GET = {'username': 'joe', 'password': '1234'}
    response = register_view(dummy_request)
    assert isinstance(response, HTTPUnauthorized)
    

def test_auth_reg_view(dummy_request):
    from ..views.auth import register_view
    response = register_view(dummy_request)
    assert response == {}


def test_auth_register_view(dummy_request):
    """register view response"""
    from ..views.auth import register_view

    dummy_request.POST = {'username': 'joe', 'password': '1234', 'email': 'joe@schmoe.com'}
    dummy_request.method = 'POST'
    response = register_view(dummy_request)
    assert response.status_code == 302


def test_auth_signup_view_instance(dummy_request):
    """HTTPFound register view POST"""
    from ..views.auth import register_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'username': 'joe', 'password': '1234', 'email': 'joe@schmoe.com'}
    dummy_request.method = 'POST'
    response = register_view(dummy_request)
    assert isinstance(response, HTTPFound)


def test_bad_reqeust_auth_register_view(dummy_request):
    """POST response status code"""
    from ..views.auth import register_view

    dummy_request.POST = {'password': 'joe', 'email': 'joe@schmoe.com'}
    dummy_request.method = 'POST'
    response = register_view(dummy_request)
    assert response.status_code == 400


def test_bad_reqeust_auth_register_view_instance(dummy_request):
    """registerview HTTPBadRequest"""
    from ..views.auth import register_view
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.POST = {'password': 'joe', 'email': 'joe@schmoe.com'}
    dummy_request.method = 'POST'
    response = register_view(dummy_request)
    assert isinstance(response, HTTPBadRequest)


def test_bad_request_method_auth_register_view(dummy_request):
    """Post register view status code"""
    from ..views.auth import register_view

    dummy_request.POST = {'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'PUT'
    response = register_view(dummy_request)
    assert response.status_code == 302


def test_bad_request_method_auth_register_view_instance(dummy_request):
    """HTTPFound register view"""
    from ..views.auth import register_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'PUT'
    response = register_view(dummy_request)
    assert isinstance(response, HTTPFound)


def test_default_portfolio_view(dummy_request, db_session, test_entry):
    """portfolio view 404"""
    from ..views.auth import detail_view
    db_session.add(test_entry)

    response = detail_view(dummy_request)
    assert response.status_code == 404


def test_portfolio_not_found(dummy_request):
    """test HTTPNotFound response"""
    from ..views.auth import detail_view
    from pyramid.httpexceptions import HTTPNotFound

    response = detail_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_default_response_stock_add_view(dummy_request):
    """verify returns dict"""
    from ..views.auth import stock_add_view

    response = stock_add_view(dummy_request)
    assert type(response) == dict


def test_default_response_stock_add_view_ii(dummy_request):
    """verify dict is empty if no stock given"""
    from ..views.auth import stock_add_view

    response = stock_add_view(dummy_request)
    assert len(response) == 0


def test_stock_add_view(dummy_request):
    """404 if not stock symbol given"""
    from ..views.auth import stock_add_view
    dummy_request.method = 'POST'
    dummy_request.POST = {}
    response = stock_add_view(dummy_request)
    assert response.status_code == 404


def test_404():
    """404 test"""
    from ..views.auth import stock_404_view
    assert stock_404_view('BINGO') == {}


def test_not_found_returns_correctly(dummy_request):
    """test not found view"""
    from ..views.notfound import notfound_view
    assert notfound_view(dummy_request) == {}


