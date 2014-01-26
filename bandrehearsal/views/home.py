from pyramid.view import view_config

@view_config(request='traversal.Home', renderer='templates/home.mako')
def home(request):
    return {}
