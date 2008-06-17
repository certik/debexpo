from debexpo.tests import *

class TestPackagesController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='packages'))
        # Test response...
