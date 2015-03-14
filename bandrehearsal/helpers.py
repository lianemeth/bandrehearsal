from pyramid.i18n import TranslationString as _
from pyramid.httpexceptions import HTTPFound
from models import DBSession
from datetime import datetime
import deform

def merge_appstruct(record, appstruct):
    '''merge a appstruct to a mapped record'''
    for key,value in appstruct.items():
        if hasattr(record, key):
            setattr(record, key, value)
    return record


def generic_edit_view(request, form, record=None, redirect='../'):
    '''a generic edit view, it must receive a request and a form.
    if record is None, will edit the request.context variable.
    default value for undefined is ../'''
    record = record or request.context
    if request.POST:
        form_items = request.POST.items()
        try:
            appstruct = form.validate(form_items)
        except deform.ValidationFailure, e:
            return {'form' : e.render(),
                    'requirements' : form.get_widget_resources()}
        record = merge_appstruct(record, appstruct)
        DBSession.merge(record)
        return HTTPFound(location=redirect)
    appstruct = record.to_appstruct()
    return {'form' : form.render(appstruct=appstruct), 
            'requirements' : form.get_widget_resources()}

def strf_appstruct(appstruct):
    for field, val in sorted(appstruct):
        if isinstance(val, datetime):
            appstruct[field] = val.strftime("%d/%m/%Y")
    return appstruct
