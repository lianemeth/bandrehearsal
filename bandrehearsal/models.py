import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session, sessionmaker,
    synonym, relationship)

from sqlalchemy.orm.exc import NoResultFound

from zope.sqlalchemy import ZopeTransactionExtension

from passlib.hash import sha256_crypt

from datetime import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    pswd = sa.Column(sa.String, nullable=False)
    login = sa.Column(sa.String, nullable=False, unique=True)
    email = sa.Column(sa.Text, nullable=False)
    phone = sa.Column(sa.Text)
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

    def __unicode__(self):
        return self.name

class Band(Base):
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

class UserBand(Base):
    __tablename__ = 'user_x_band'

    band_id = sa.Column(sa.Integer, sa.ForeignKey('bands.id'), primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), primary_key=True)
    role = sa.Column(sa.Text)

    def __unicode__(self):
        return self.name
