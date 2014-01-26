class BandResource(dict):
    
    def __init__(self, name, parent, *args, **kwargs):
        self.__name__ = name
        self.__parent__ = parent
        super(BandResource, self).__init__(*args, **kwargs)

def get_root(request):
    root = BandResource('/', None)
