import unittest

from pyramid import testing
from datetime import datetime
from ..models import DBSession


class TestModels(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from ..models import Base
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

    def test_mixin(self):
        from ..models import Mixin
        class FakeModel(Mixin):
            def __init__(self):
                self.field_1 = 'a'
                self.field_2 = 'b'
                self._sa_field = 'c'
                self.hide_fields = ['field_2']

        model = FakeModel()
        self.assertEqual(model.to_appstruct(), 
                {'field_1': 'a', 'field_2': 'b'})
        self.assertEqual(model.fields_to_display(),
                {'field_1': 'a'})

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
                members=[user1, user2])
        DBSession.add(band)
        DBSession.flush()
        self.assertEqual(user1.bands, [band])
        self.assertEqual(user2.bands, [band])
        self.assertEqual(band.members, [user1, user2])

    def test_event(self):
        from ..models import (User, Band, Event,
                EventComment)
        user1 = User(login='neobula',
                password='pswd',
                email='some@mail.com')
        DBSession.add(user1)
        DBSession.flush()
        band = Band(name='The Arthur Conan Doyle Hand Cream',
                description='Moisturizing rock music',
                members=[user1])
        DBSession.add(band)
        DBSession.flush()
        event = Event(time=datetime.now(),
                place='Silver Rocket',
                band=band)
        DBSession.add(event)
        DBSession.flush()
        self.assertTrue(event.name)
        self.assertEqual(event.band_id, band.id)
        self.assertEqual(event.name, event.default_name)
        comment = EventComment(event_id=event.id,
                user_id=user1.id,
                content="...content")
        self.assertEqual(comment.content, "...content")

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()
