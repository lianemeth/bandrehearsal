from .models import *


class Resource(dict):

    def __init__(self, name, parent, *args, **kwargs):
        self.__name__ = name
        self.__parent__ = parent
        super(Resource, self).__init__(*args, **kwargs)


class ModelResource(Resource):
    '''A resource class that will return
    a cls.model object'''

    model = None

    def __getitem__(self, item):
        if item == 'new':
            return self.model()
        return DBSession.query(self.model).get(item)


class UsersResource(Resource):

    def __getitem__(self, item):
        if item == 'activate':
            return ActivationResource('activate', self)
        return DBSession.query(self.User).get(item)



class BandResource(ModelResource):
    model = Band


def get_root(request):
    root = Resource('/', None)
    root['user'] = UsersResource('user', root)
    root['band'] = BandResource('band', root)
    return root
