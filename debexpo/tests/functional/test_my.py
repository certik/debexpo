from debexpo.tests import *

class TestMyController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='my'))
        # Test response...
