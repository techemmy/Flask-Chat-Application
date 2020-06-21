import unittest
import os
from application import create_app
from models import db, User

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
        app.app_context().push()
        db.create_all()

    def tearDown(self):
        db.session.remove()

    def test_homepage(self):
        """ test user not connected page """
        request = self.app.get("/")
        self.assertEqual(request.status_code, 200)

    def test_registered_user(self):
        user = User(firstname="Test", lastname="Lase", username="User",
                    email="Email@gmail.com", password="nvmmme", terms=True)
        db.session.add(user)
        self.assertIn(user, db.session)


if __name__ == '__main__':
    unittest.main()
