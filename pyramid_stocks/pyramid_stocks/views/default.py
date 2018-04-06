from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config
from ..sample_data import MOCK_DATA


@view_config(
    route_name='home', 
    renderer='../templates/base.jinja2',
    request_method='GET')
def home_view(request):
    return {}


@view_config(
    route_name='portfolio', 
    renderer='../templates/portfolio.jinja2',
    request_method='GET')
def portfolio_view(request):   
        return {
            'companies': MOCK_DATA
        }


@view_config(
    route_name='auth', 
    renderer='../templates/login.jinja2')
def register_view(request):
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
    return {}


@view_config(route_name='detail', renderer='../templates/detail.jinja2')
def detail_view(request):
    return {}


@view_config(route_name='404', renderer='../templates/404.jinja2')
def stock_404_view(request):
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
