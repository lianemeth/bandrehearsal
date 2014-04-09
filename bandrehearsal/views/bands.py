from pyramid.view import view_config
from ..models import Band, DBSession
from ..helpers import generic_edit_view

import colander
import deform
from pyramid.i18n import TranslationString as _


class BandSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.String(),
        description=_("The band's name"))
    description = colander.SchemaNode(
        colander.String(),
        description=_("Something about your band"))

    class Member(colander.SequenceSchema):
        member = colander.SchemaNode(
            colander.String(),
            validator=colander.Email(),
            description=_("Type the user e-mail account"))
    members = Member()


class EditBandView(object):

    def __init__(self, request):
        self.request = request
        self.band = request.context

    @view_config(context=Band, name='edit',
            renderer='bandrehearsal:templates/band.mako')
    def view(request):
        if request.POST:
            form_items = request.POST.items()
            try:
                appstruct = form.validate(form_items)
            except deform.ValidationFailure, e:
                return {'form' : e.render(),
                        'requirements' : form.get_widget_resources()}
            self.process_form(appstruct)
            return HTTPFound(location='../')
        appstruct = record.to_appstruct()
        return {'form' : form.render(appstruct=appstruct), 
                'requirements' : form.get_widget_resources()}

        def process_form(self, appstruct):
            DBSession.merge(self.band)
