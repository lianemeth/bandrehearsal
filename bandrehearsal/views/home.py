from pyramid.view import view_config
from ..models import DBSession, Event


def format_band_info(bands, events):
    out_d = {}
    for band in bands:
        out_d[band] = {'events': []}
        for event in events:
            if event.band_id == band.id:
                out_d[band]['events'].append(event)
    return out_d


@view_config(route_name='home', renderer='bandrehearsal:templates/home.mako')
def home(request):
    '''BandRehearsal home page includes all relevant information about your
    user'''
    bands_d = {}
    if request.user:
        bands = request.user.bands
        bands_ids = [band.id for band in bands]
        events = []
        if bands_ids:
            events = DBSession.query(Event).filter(
                Event.band_id.in_(bands_ids))
        bands_d = format_band_info(bands, events)
    return {'bands': bands_d}
