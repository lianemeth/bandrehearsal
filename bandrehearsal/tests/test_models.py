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
        user = User(login='someone',
                password='pswd',
                email='some@mail.com')
        DBSession.add(user)
        DBSession.flush()
        self.assertNotEqual('pswd', user.password)
        p1 = user.password
        user.password = 'new pswd'
        p2 = user.password
        self.assertNotEqual('new pswd', user.password)
        self.assertTrue(user.check_password('new pswd'))
        self.assertNotEqual(p1, p2)
        self.assertEqual(User.log('someone', 'new pswd'), user)

    def test_bands(self):
        from ..models import User, Band
        user1 = User(login='brony',
                password='pswd',
                email='some@mail.com')
        user2 = User(login='someone',
                password='123',
                email='pineapple@uol.com')
        DBSession.add(user1)
        DBSession.add(user2)
        DBSession.flush()
        band = Band(name='The Mini Ponies',
                description='A post-rock brony ',
                members = [user1, user2])
        DBSession.add(band)
        DBSession.flush()
        self.assertEqual(user1.bands, [band])
        self.assertEqual(user2.bands, [band])
        self.assertEqual(band.members, [user1, user2]) 

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()
