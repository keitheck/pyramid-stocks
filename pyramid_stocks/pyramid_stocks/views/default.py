from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config
from ..sample_data import MOCK_DATA
import json
import requests


API_URL = 'https://api.iextrading.com/1.0'


@view_config(
    route_name='home', 
    renderer='../templates/base.jinja2',
    request_method='GET')
def home_view(request):
    """returns home page"""
    return {}


@view_config(
    route_name='portfolio', 
    renderer='../templates/portfolio.jinja2',
    request_method='GET')
def portfolio_view(request):
    """Returns user portfolio data""" 
    return {
        'companies': MOCK_DATA
        }


@view_config(
    route_name='auth', 
    renderer='../templates/login.jinja2')
def register_view(request):
    """GET method supports user sign in and POST method support creation of username and password"""
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']
            print('User: {}, Pass: {}'.format(username, password))

            return HTTPFound(location=request.route_url('portfolio'))
        
        except KeyError:
            return {}

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        print('User {}, Pass {}, email {}'.format(username, password, email))   
        
        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()


@view_config(route_name='stock-add', renderer='../templates/stock-add.jinja2')
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
            data = response.json()
            MOCK_DATA.append(data)
            return HTTPFound(location=request.route_url('portfolio'))

        except:
            pass

    else:
        raise HTTPNotFound()


@view_config(route_name='detail', renderer='../templates/detail.jinja2')
def detail_view(request):
    """displays stock details on an individual stock to the detail page"""
    try:
        symbol = request.matchdict['symbol']
    
    except KeyError:
        return HTTPNotFound()

    for company in MOCK_DATA:
        if company['symbol'] == symbol:
            return {'company': company}


@view_config(route_name='404', renderer='../templates/404.jinja2')
def stock_404_view(request):
    """returns 404 page"""
    return {}    
        






# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def my_view(request):
#     try:
#         query = request.dbsession.query(MyModel)
#         one = query.filter(MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)
#     return {'one': one, 'project': 'pyramid_stocks'}


# db_err_msg = """\
# Pyramid is having a problem using your SQL database.  The problem
# might be caused by one of the following things:

# 1.  You may need to run the "initialize_pyramid_stocks_db" script
#     to initialize your database tables.  Check your virtual
#     environment's "bin" directory for this script and try to run it.

# 2.  Your database server may not be running.  Check that the
#     database server referred to by the "sqlalchemy.url" setting in
#     your "development.ini" file is running.

# After you fix the problem, please restart the Pyramid application to
# try it again.
# """
