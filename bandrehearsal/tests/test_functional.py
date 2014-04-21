import unittest

import ConfigParser


def load_settings(confpath, basepath):
    '''load settings'''
    default_key = {'here': basepath}
    configparser = ConfigParser.ConfigParser(default_key)
    if not configparser.read(confpath):
        raise ConfigParser.Error('Could not open %s' % confpath)
    settings = {}
    for key, value in configparser.items('app:main'):
        settings[key] = value
    return settings


class FunctionalTests(unittest.TestCase):

    def setUp(self):
        from .. import main
        settings = load_settings('development.ini', './')
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue('BandRehearsal' in res.body)
