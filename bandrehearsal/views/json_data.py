from ..models import User
from pyramid.view import view_config

@view_config(context=User, name='events', renderer="json") 
def get_user_events(request, context):
    events = {}
    for event in context.events:
        events[event] = format_event(event)
    return events
