import unittest
import os
from application import create_app

TEST_DB = 'test.db'


class HookTest(unittest.TestCase):
    """ Test to confirm app works """
    def test_index(self):
        """ ensure that flask setup is OK """
        tester = create_app().test_client(self)
        response = tester.get("/", content_type='text/html')
        self.assertEqual(response.status_code, 200)


class AuthenticationTests(unittest.TestCase):
    """ Test for authentication """
    def setUp(self):
        """ Setup a blank test db before each test """
        basedir = os.path.abspath(os.path.dirname(__file__))
        app = create_app({
                         'TESTING': True,
                         'ENV': 'test',
                         'SQLALCHEMY_DATABASE_URI': 'sqlite:///' +
                         os.path.join(basedir, TEST_DB)
                         })
        self.app = app.test_client()


if __name__ == '__main__':
    unittest.main()
