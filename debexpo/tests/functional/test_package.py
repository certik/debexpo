from debexpo.tests import *

class TestPackageController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='package'))
        # Test response...
