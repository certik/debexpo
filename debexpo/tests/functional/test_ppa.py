from debexpo.tests import *

class TestPpaController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='ppa'))
        # Test response...
