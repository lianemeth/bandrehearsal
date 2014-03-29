from pyramid.view import view_config
from pyramid.security import authenticated_userid


@view_config(route_name='home', renderer='bandrehearsal:templates/home.mako')
def home(request):
    return {}
