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
        DBSession.remove()

    def test_login_view(self):
        from ..views.login import LoginView
        from ..models import User
        user = User(login='user',
                password='password',
                email='user@user.com')
        DBSession.add(user)
        DBSession.flush()
        request = testing.DummyRequest()
        request.POST = {'user': 'user',
                        'password': 'password'}
        loginview = LoginView(request)
        self.assertIsInstance(loginview.login(), HTTPFound)
        request1 = testing.DummyRequest()
        request1.POST = {'user': 'ussjak',
                        'password': 'password123'}
        loginview1 = LoginView(request1)
        res = loginview1.login()
        self.assertTrue(res['fail'])
        self.assertTrue('requirements' in res)
        self.assertTrue('form' in res)

    def test_home(self):
        from ..views.home import home
        self.config.testing_securitypolicy(userid='user',
                permissive=False)
        request = testing.DummyRequest()
        self.assertTrue(home(request) is not None)

    def test_list_users(self):
        from ..models import User
        from ..views.login import list_users
        user1 = User(login='user',
                password='password',
                email='user@user.com')
        user2 = User(login='user2',
                password='password',
                email='user2@user.com')
        DBSession.add(user1)
        DBSession.add(user2)
        DBSession.flush()
        request = testing.DummyRequest()
        res = list_users(request)
        self.assertTrue(user1 in res['list'])
        self.assertTrue(user1 in res['list'])

    def test_delete_user(self):
        from ..models import User
        from ..views.login import delete_user
        user = User(login='user',
                password='password',
                email='user@user.com')
        DBSession.add(user)
        DBSession.flush()
        id = user.id
        request = testing.DummyRequest()
        request.context = user
        delete_user(request)
        self.assertFalse(DBSession.query(User).get(id).active)

    def test_edit_user(self):
        from ..models import User
        from ..views.login import edit_user
        user = User(login='user',
                password='password',
                email='user@user.com')
        DBSession.add(user)
        DBSession.flush()
        id = user.id
        request = testing.DummyRequest()
        request.context = user
        res = edit_user(request)
        self.assertTrue(res['form'])

    def test_view_user(self):
        from ..models import User
        from ..views.login import view_user
        user = User(login='user',
                password='password',
                email='user@user.com')
        DBSession.add(user)
        DBSession.flush()
        request = testing.DummyRequest()
        request.context = user
        res = view_user(request)
        self.assertEqual(res['user'], user)
