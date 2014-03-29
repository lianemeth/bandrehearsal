from .models import *


class BandResource(dict):

    def __init__(self, name, parent, *args, **kwargs):
        self.__name__ = name
        self.__parent__ = parent
        super(BandResource, self).__init__(*args, **kwargs)


class UsersResource(BandResource):

    def __getitem__(self, item):
        return DBSession.query(User).get(item)


def get_root(request):
    root = BandResource('/', None)
    root['user'] = UsersResource('user', root)
    return root
