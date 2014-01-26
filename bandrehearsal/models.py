import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session, sessionmaker,
    synonym, relationship)


from zope.sqlalchemy import ZopeTransactionExtension

from passlib.hash import sha256_crypt

from datetime import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    pswd = sa.Column(sa.String, nullable=False)
    login = sa.Column(sa.String, nullable=False, unique=True)
    email = sa.Column(sa.Text, nullable=False)
    phone = sa.Column(sa.Text)
    creation = sa.Column(sa.DateTime, default=datetime.now)

    def __init__(self, password, login, email, phone=None, name=None):
        self.password = password
        self.login = login
        self.email = email
        self.phone = phone
        self.name = name

    @property
    def password(self):
        return self.pswd

    @password.setter
    def password(self, value):
        self.pswd = sha256_crypt.encrypt(value)

    password = synonym("pswd", descriptor=password)

    def check_password(self, passwd):
        return sha256_crypt.verify(passwd, self.password)


class Band(Base):
    __tablename__ = 'band'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    description = sa.Column(sa.Text)
    creation = sa.Column(sa.DateTime, default=datetime.now)
    
    members = relationship("User",
            secondary="user_x_band",
            backref="bands")


class UserBand(Base):
    __tablename__ = 'user_x_band'

    band_id = sa.Column(sa.Integer, sa.ForeignKey('band.id'), primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
    role = sa.Column(sa.Text)
