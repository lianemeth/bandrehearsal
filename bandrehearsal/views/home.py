from pyramid.view import view_config
from pyramid.security import authenticated_userid


@view_config(route_name='home', renderer='bandrehearsal:templates/home.mako')
def home(request):
    user = authenticated_userid(request) or None
    return {'user': user}
