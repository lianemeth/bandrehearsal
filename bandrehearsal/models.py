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

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Mixin(object):

    def to_appstruct(self):
        return dict([(k, self.__dict__[k]) for k in sorted(self.__dict__) \
            if '_sa_' != k[:4]])

    @classmethod
    def choices(cls, with_empty=False):
        query = DBSession.query(cls)
        pk = class_mapper(cls).primary_key[0].name
        l = [ (getattr(record ,pk), unicode(record)) for record in query]
        if with_empty:
            l = [('','')] + l
        return l


class User(Base, Mixin):
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
    login = sa.Column(sa.String, nullable=False, unique=True)
    email = sa.Column(sa.Text, nullable=False)
    phone = sa.Column(sa.Text)
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

    class WrongCredential(Exception):
        pass

    @classmethod
    def log(cls, user_login, password):
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
        return DBSession.query(User).filter_by(active=True)

    def __unicode__(self):
        return self.name


def get_user(request):
    login = unauthenticated_userid(request)
    if login is not None:
        return User.get_by_login(login)


class UserBand(Base, Mixin):
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

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    description = sa.Column(sa.Text)
    creation = sa.Column(sa.DateTime, default=datetime.now)

    members = relationship("User",
                    secondary="user_x_band",
                    backref="bands")

    def __unicode__(self):
        return self.name
