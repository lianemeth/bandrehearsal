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

from uuid import uuid4

# initialize sqlalchemy Session
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
# initialize declarative base, for sqlalchemy orm
Base = declarative_base()


class Mixin(object):
    '''A mixin that add some features to sqlalchemy orm objects'''

    def to_appstruct(self):
        '''returns a appstruct for colander'''
        return dict([(k, self.__dict__[k]) for k in sorted(self.__dict__) \
            if '_sa_' != k[:4]])

    @classmethod
    def choices(cls, with_empty=False):
        '''return the elements of mapped table as a list of tuples
        in the (id, name) format'''
        query = DBSession.query(cls)
        pk = class_mapper(cls).primary_key[0].name
        l = [ (getattr(record ,pk), unicode(record)) for record in query]
        if with_empty:
            l = [('','')] + l
        return l


class User(Base, Mixin):
    '''an user of the system'''

    __tablename__ = 'users'

    @property
    def __acl__(self):
        acl = [(Allow, 'admin', 'edit')]
        acl += (Allow, self.login, 'edit')
        acl += (Allow, Authenticated, 'view')
        return acl

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    pswd = sa.Column(sa.String, nullable=False)
    login = sa.Column(sa.String, nullable=False, unique=True, index=True)
    email = sa.Column(sa.Text, nullable=False, unique=True, index=True)
    phone = sa.Column(sa.Text)
    activation_uid = sa.Column(sa.Text)
    active = sa.Column(sa.Boolean, default=True)
    creation = sa.Column(sa.DateTime, default=datetime.now)

    @property
    def password(self):
        return self.pswd

    @password.setter
    def password(self, value):
        self.pswd = sha256_crypt.encrypt(value)

    password = synonym("pswd", descriptor=password)

    def check_password(self, passwd):
        return sha256_crypt.verify(passwd, self.password)

    @classmethod
    def new_registration_user(cls, email):
        uid1 = str(uuid4())
        uid2 = str(uuid4())
        return User(pswd=uid1, 
                login=uid2,
                email=email,
                activation_uid=uid2,
                active=False)

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
            user = DBSession.query(User).filter(user_login == User.login,
                    User.active == True).one()
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

    @classmethod
    def has_email_registered(self, email):
        '''check if it exists an User registered with this e-mail
        if it does, return him, else return None'''
        try:
            user = DBSession.query(User).filter_by(email=email).one()
        except NoResultFound:
            return None
        return user

    @classmethod
    def activate(cls, uid):
        try:
            user = DBSession.query(User).filter_by(activation_uid=uid).one()
        except NoResultFound as exc:
            raise exc
        user.active = True
        DBSession.merge(user)
        return user

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

    members = relationship("User",
                    secondary="user_x_band",
                    backref="bands")

    def __unicode__(self):
        return self.name
