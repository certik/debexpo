from debexpo.tests import *

class TestRegisterController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='register'))
        # Test response...
