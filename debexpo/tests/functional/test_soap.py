from debexpo.tests import *

class TestSoapController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='soap'))
        # Test response...
