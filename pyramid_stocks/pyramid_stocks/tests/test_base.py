import pytest
from pyramid import testing
from .models.meta import Base
from ..models import Account
from ..models import My_stocks

"""conftest moved here per Scott to try to get tests to run"""
@pytest.fixture
def dummy_request(db_session):
    """Create a dummy GET request with a dbsession."""
    return testing.DummyRequest(dbsession=dbsession)

"""end fixtures"""



def test_stock_view(dummy_request):
    from ..views.stock import stock_view
    dummy_request.GET = {'symbol':'ABC'}
    assert stock_view(dummy_request)['company'] == 'ABC'
    