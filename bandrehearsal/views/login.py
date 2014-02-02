from pyramid.view import view_config

from ..models import DBSession, User
from pyramid.security import remember
from pyramid.httpexceptions import HTTPFound

import colander
import deform

class LoginSchema(colander.Schema):
    user = colander.SchemaNode(
            colander.String(),
            description=u"Type your user")
    password = colander.SchemaNode(
            colander.String(),
            widget = deform.widget.PasswordWidget(size=20),
            description = u"Type your password")


class LoginView(object):
    
    def __init__(self, request):
        self.request = request
        self.fail = False
        self.next_page = request.params.get('next') or request.route_url('home')
        self.buttons = ('submit', )

    @view_config(route_name='login', renderer='templates/login.mako')
    def login(self):
        if self.request.POST:
            user = self.request.POST.get('user', '')
            passwd = self.request.POST.get('password', '')
            try:
                logged_user = User.log(user, passwd)
            except User.WrongCredential:
                self.fail = True
            else:
                headers = remember(self.request, logged_user.id)
                return HTTPFound(location=next, headers=headers)
        return { 'form' : self.login_form(),
                 'next' : self.next_page,
                 'fail' : self.fail }

    def login_form(self):
        return deform.Form(LoginSchema(), buttons=self.buttons)
