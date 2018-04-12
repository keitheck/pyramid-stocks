from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPUnauthorized, HTTPBadRequest
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
from sqlalchemy.exc import DBAPIError, IntegrityError
from pyramid.view import view_config
from ..models import My_stocks
from ..models import Account
from ..models.association import association_table
from . import DB_ERR_MSG
import json
import requests

API_URL = 'https://api.iextrading.com/1.0'

# @view_config(
#     route_name='home', 
#     renderer='../templates/base.jinja2',
#     request_method='GET')
# def home_view(request):
#     """returns home page"""
#     return {}


@view_config(
    route_name='portfolio', 
    renderer='../templates/portfolio.jinja2',
    request_method='GET')
def portfolio_view(request):
    """Returns user portfolio data"""
    try:
        query = request.dbsession.query(My_stocks)
        user_stocks = query.filter(Account.username == request.authenticated_userid).first()

    except DBAPIError:
        return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

    return {'companies': user_stocks}    


@view_config(
    route_name='auth', 
    renderer='../templates/login.jinja2',
    permission=NO_PERMISSION_REQUIRED)
def register_view(request):
    """GET method supports user sign in and POST method support creation of username and password"""
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']
            
        except KeyError:
            return {}

        is_authenticated = Account.check_credentials(request, username, password)
        if is_authenticated[0]:
            headers = remember(request, userid=username)
            return HTTPFound(location=request.route_url('portfolio'), headers=headers)
        else:
            return HTTPUnauthorized()    
    
        return HTTPFound(location=request.route_url('auth'))

    if request.method == 'POST':
        # import pdb ; pdb.set_trace()
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

        except KeyError:
            return HTTPBadRequest()

        try:
            instance = Account(
                account_id=request.authenticated_userid,
                username=username,
                email=email,
                password=password,
            )

            headers = remember(request, userid=instance.username)
            request.dbsession.add(instance)
            request.dbsession.flush()

        except IntegrityError:
            raise HTTPNotFound('username already taken')

        return HTTPFound(location=request.route_url('portfolio'), headers=headers)

        # except DBAPIError:
        #     return Response(DB_ERR_MSG, content_type='text/plain', status=500)

    # return HTTPNotFound()
    return HTTPFound(location=request.route_url('auth'))


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)


@view_config(route_name='stock', renderer='../templates/stock.jinja2')
def stock_add_view(request):
    """Get and Post methods to display requested stock info and selectively add to portfolio"""
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        
        except KeyError:
            return {}

        try:
            response = requests.get(API_URL + "/stock/{}/company".format(symbol))
            data = response.json()

        except json.decoder.JSONDecodeError:
            return {}
            
        return {'company': data}

    if request.method == 'POST':
        try:
            stock = request.POST['add-stock']
            response = requests.get(API_URL + "/stock/{}/company".format(stock))
            
            response = response.json()
             
        except KeyError:
            return HTTPNotFound()

        if request.dbsession.query(My_stocks).filter(My_stocks.symbol == stock).count(): 
            return HTTPFound(location=request.route_url('portfolio'))

        else:
            request.dbsession.add(My_stocks(**response))

    return HTTPFound(location=request.route_url('portfolio'))


@view_config(route_name='detail', renderer='../templates/detail.jinja2')
def detail_view(request):
    """displays stock details on an individual stock to the detail page"""
    try:
        symbol = request.matchdict['symbol']

    except KeyError:
        return HTTPNotFound()

    query = request.dbsession.query(My_stocks)

    for company in query.all():
        if company.symbol == symbol:
            return {'company': company}


@view_config(route_name='404', renderer='../templates/404.jinja2')
def stock_404_view(request):
    """returns 404 page"""
    return {}    
        


