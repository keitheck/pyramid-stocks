from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED


@view_config(
    route_name='home', 
    renderer='../templates/base.jinja2',
    request_method='GET',
    permission=NO_PERMISSION_REQUIRED)
def home_view(request):
    """returns home page"""
    return {}


# from pyramid.response import Response
# from pyramid.httpexceptions import HTTPFound, HTTPNotFound
# from pyramid.view import view_config
# from ..sample_data import MOCK_DATA
# from sqlalchemy.exc import DBAPIError
# from ..models import My_stocks
# from ..models import Account
# from . import DB_ERR_MSG
# import json
# import requests