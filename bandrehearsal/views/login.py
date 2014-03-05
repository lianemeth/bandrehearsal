from pyramid.view import view_config

from ..models import User
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

    @view_config(route_name='login', renderer='bandrehearsal:templates/login.mako')
    def login(self):
        if self.request.POST:
            user = self.request.POST.get('user', '')
            passwd = self.request.POST.get('password', '')
            try:
                logged_user = User.log(user, passwd)
            except User.WrongCredential:
                self.fail = True
            else:
                headers = remember(self.request, logged_user.login)
                return HTTPFound(location=self.next_page, headers=headers)
        form = self.login_form()
        return { 'form' : form.render(),
                 'requirements' : form.get_widget_resources(),
                 'next' : self.next_page,
                 'fail' : self.fail }

    def login_form(self):
        return deform.Form(LoginSchema(), buttons=self.buttons)


@view_config(name='list', context=User,
    renderer='bandrehearsal:templates/users.mako', permission='edit')
def list_users(request):
    users =  User.actives()
    return {'list' : users}


@view_config(name='delete', context=User,
    renderer='bandrehearsal:templates/users.mako', permission='edit')
def delete_user(request):
    request.context.active = False
    return {'status' : 'success'}


@view_config(name='edit', context=User,
    renderer='bandrehearsal:templates/users.mako', permission='edit')
def edit_user(request):
    return  {}


@view_config(name='view', context=User,
    renderer='bandrehearsal:templates/users.mako', permission='view')
def view_user(request):
    return {'user' : request.context}
