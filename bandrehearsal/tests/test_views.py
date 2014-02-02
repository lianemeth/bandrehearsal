import unittest
from pyramid import testing
from pyramid.httpexceptions import HTTPFound
from ..models import DBSession


class TestViews(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.add_route('home', '/')
        self.config.add_route('login', '/login')
        self.config.add_route('select_band', '/select')
        self.config.add_route('app', '/{band}/*traverse')
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from ..models import Base
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

    def tearDown(self):
        testing.tearDown()

    def test_login_view(self):
        from ..views.login import LoginView
        from ..models import User
        user = User(login='user',
                password='password',
                email='user@user.com')
        DBSession.add(user)
        DBSession.flush()
        request = testing.DummyRequest()
        request.POST = {'user' : 'user',
                        'password' : 'password'}
        loginview = LoginView(request)
        self.assertIsInstance(loginview.login(), HTTPFound)
        request1 = testing.DummyRequest()
        request1.POST = {'user' : 'ussjak',
                        'password' : 'password123'}
        loginview1 = LoginView(request1)
        res = loginview1.login()
        self.assertTrue(res['fail'])

    def test_home(self):
        from ..views.home import home
        self.config.testing_securitypolicy(userid='user',
                permissive=False)
        request = testing.DummyRequest()
        self.assertTrue(home(request)['user'])
        self.config.testing_securitypolicy(userid='',
                permissive=False)
        request = testing.DummyRequest()
        self.assertFalse(home(request)['user'])

