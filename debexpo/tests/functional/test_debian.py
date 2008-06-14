from debexpo.tests import *

class TestDebianController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='debian'))
        # Test response...
