from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED


@view_config(
    route_name='home',
    renderer='../templates/index.jinja2',
    permission=NO_PERMISSION_REQUIRED)
def home_view(request):
    """index page"""
    return {}