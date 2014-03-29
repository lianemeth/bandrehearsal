from pyramid.i18n import TranslationString as _
from pyramid.httpexceptions import HTTPFound
import deform

def merge_appstruct(record, appstruct):
    for key,value in appstruct.items():
        if hasattr(record, key):
            setattr(record, key, value)
    return record


def generic_edit_view(request, record=None, redirect='../'):
    record = record or request.context
    form = deform.Form(record.__colanderalchemy__, 
            buttons=(_('send'),))
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
