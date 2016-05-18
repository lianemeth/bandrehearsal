import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session, sessionmaker,
    synonym, relationship,
    class_mapper)

from sqlalchemy.orm.exc import NoResultFound

from zope.sqlalchemy import ZopeTransactionExtension

from passlib.hash import sha256_crypt

from pyramid.security import Allow, Authenticated, unauthenticated_userid

from datetime import datetime

# initialize sqlalchemy Session
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
# initialize declarative base, for sqlalchemy orm
Base = declarative_base()


class Mixin(object):
    '''A mixin that add some features to sqlalchemy orm objects'''

    def to_appstruct(self):
        '''returns a appstruct for colander'''
        return dict((k, self.__dict__[k]) for k in sorted(self.__dict__)
            if '_sa_' != k[:4] and k != 'hide_fields')

    def fields_to_display(self):
        hide_fields = []
        if hasattr(self, 'hide_fields'):
            hide_fields += self.hide_fields
        return dict((field, val) for field, val in self.to_appstruct().items()
                if field not in hide_fields)

    @classmethod
    def choices(cls, with_empty=False):
        '''return the elements of mapped table as a list of tuples
        in the (id, name) format'''
        query = DBSession.query(cls)
        pk = class_mapper(cls).primary_key[0].name
        l = [(getattr(record, pk), unicode(record)) for record in query]
        if with_empty:
            l = [('', '')] + l
        return l


class User(Base, Mixin):
    '''an user of the system'''

    __tablename__ = 'users'

    @property
    def __acl__(self):
        return [(Allow, 'admin', 'edit'),
            (Allow, self.login, 'edit'),
            (Allow, Authenticated, 'view')]

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    pswd = sa.Column(sa.String, nullable=False)
    login = sa.Column(sa.String, nullable=False, unique=True)
    email = sa.Column(sa.Text, nullable=False)
    phone = sa.Column(sa.Text)
    active = sa.Column(sa.Boolean, default=True)
    creation = sa.Column(sa.DateTime, default=datetime.now)
    hide_fields = ('pswd',)

    @property
    def password(self):
        return self.pswd

    @password.setter
    def password(self, value):
        self.pswd = sha256_crypt.encrypt(value)

    password = synonym("pswd", descriptor=password)

    def check_password(self, passwd):
        return sha256_crypt.verify(passwd, self.password)

    class WrongCredential(Exception):
        pass

    @classmethod
    def log(cls, user_login, password):
        '''try to find a user by it's login and checks
        if the password matches the stored one.
        If everything is right, returns the requested user.
        Case the user was not found or the password didn't match,
        returns a WrongCredential exception'''
        try:
            user = DBSession.query(User).filter(user_login == User.login).one()
        except NoResultFound:
            raise cls.WrongCredential
        if user.check_password(password):
            return user
        else:
            raise cls.WrongCredential

    @classmethod
    def get_by_login(cls, login):
        return DBSession.query(User).filter_by(login=login).one()

    @classmethod
    def actives(cls):
        '''return all active users'''
        return DBSession.query(User).filter_by(active=True)

    def __unicode__(self):
        return self.name


def get_user(request):
    '''If we receive a logged request, it returns the
    current user'''
    login = unauthenticated_userid(request)
    if login is not None:
        return User.get_by_login(login)


class UserBand(Base, Mixin):
    '''many to many relationship table
    for users and bands.
    Each user can be in many different bands,
    and can have different roles in each band.
    For instance, a User can be a singer in a band
    but a guitar player in another band.'''

    __tablename__ = 'user_x_band'

    band_id = sa.Column(sa.Integer, sa.ForeignKey('bands.id'),
            primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'),
            primary_key=True)
    role = sa.Column(sa.Text)

    def __unicode__(self):
        return self.name


class Band(Base, Mixin):
    __tablename__ = 'bands'
    '''A music band, that is composed by it's members'''

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    description = sa.Column(sa.Text)
    creation = sa.Column(sa.DateTime, default=datetime.now)
    active = sa.Column(sa.Boolean, default=True)

    members = relationship("User",
                    secondary="user_x_band",
                    backref="bands")

    def __unicode__(self):
        return self.name


class EventType(Base, Mixin):
    '''A type of event, can be a gig, a rehearsal
    or idk.
    '''
    __tablename__ = 'event_types'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)

    def __unicode__(self):
        return self.name


class Event(Base, Mixin):
    '''An event, with a band, in a place, a reason,
    and that sort of thing.
    '''
    __tablename__ = 'events'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, default='')
    time = sa.Column(sa.DateTime)
    place = sa.Column(sa.Text)
    band_id = sa.Column(sa.Integer, sa.ForeignKey('bands.id'))
    creation = sa.Column(sa.DateTime, default=datetime.now)
    active = sa.Column(sa.Boolean, default=True)
    band = relationship("Band", backref="events")

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self.name = self.name if self.name else self.default_name

    @property
    def default_name(self):
        return u'{0} {1} {2}'.format(self.time, self.place, self.band)

    def __unicode__(self):
        return self.name


class EventComment(Base, Mixin):
    '''A comment attached to an Event'''

    __tablename__ = 'event_comments'

    id = sa.Column(sa.Integer, primary_key=True)
    event_id = sa.Column(sa.Integer, sa.ForeignKey('events.id'),
            nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'),
            nullable=False)
    content = sa.Column(sa.Text, nullable=True)
    active = sa.Column(sa.Boolean, default=True)
    creation = sa.Column(sa.DateTime, default=datetime.now)
