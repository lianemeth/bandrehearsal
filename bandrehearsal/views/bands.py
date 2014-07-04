from pyramid.view import view_config
from ..models import Band, DBSession, User
from ..helpers import generic_edit_view
from ..mailers import NewBandMailer, RegistrationMailer

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
        email = colander.SchemaNode(
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
    def view(self):
        form = deform.Form(BandSchema(), buttons=('Submit',))
        if self.request.POST:
            form_items = self.request.POST.items()
            try:
                appstruct = form.validate(form_items)
            except deform.ValidationFailure, e:
                return {'form' : e.render(),
                        'requirements' : form.get_widget_resources()}
            self.process_form(appstruct)
            return HTTPFound(location='../')
        appstruct = self.band.to_appstruct()
        return {'form' : form.render(appstruct=appstruct), 
                'requirements' : form.get_widget_resources()}

    def process_form(self, appstruct):
        # for each member in member list
        for member in appstruct['members']:
            user = User.has_email_registered(member)
            # if e-mail is registered, send notification to owner
            # if e-mail is not registered, send registration e-mail and
            # create new inactive user
            if user is None:
                user = User.new_registration_user(member)
                DBSession.add(user)
                mailer = RegistrationMailer(self.request, member)
            else:
                mailer = NewBandMailer(member, request=self.request,
                        user=user, band=self.band)
            self.band.members.append(user)
            mailer.send()
        DBSession.merge(self.band)
