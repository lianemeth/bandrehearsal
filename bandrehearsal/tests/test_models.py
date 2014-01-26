import unittest

from pyramid import testing

from ..models import DBSession

class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from ..models import Base
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

    def test_user(self):
        from ..models import User
        user = User(login='user',
                password='pswd',
                email='some@mail.com')
        DBSession.add(user)
        self.assertNotEqual('pswd', user.password)
        p1 = user.password
        user.password = 'new pswd'
        p2 = user.password
        self.assertNotEqual('new pswd', user.password)
        self.assertNotEqual(p1, p2)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()
