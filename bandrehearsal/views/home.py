from pyramid.view import view_config


@view_config(route_name='home', renderer='bandrehearsal:templates/home.mako')
def home(request):
    '''BandRehearsal home page includes all relevant information about your
    user'''
    bands = None
    if request.user:
        bands = request.user.bands
    return {'bands': bands}
