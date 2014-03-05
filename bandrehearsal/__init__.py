from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy import engine_from_config

from .models import DBSession, Base
from .traversal import get_root


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authn_policy = AuthTktAuthenticationPolicy(
            settings['bandrehearsal.secret_key'],
            hashalg='sha512')
    config = Configurator(settings=settings, root_factory=get_root)
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform', 'deform:static')
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('select_band', '/select')
    config.add_route('app', '/{band}/*traverse')
    config.scan()
    return config.make_wsgi_app()
