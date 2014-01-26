from pyramid.view import view_config

from .models import DBSession

@view_config(request='traversal.Login', renderer='templates/login.mako')
def login(request):
    return {}
