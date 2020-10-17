import unittest
import os
from hook import create_app
from hook.models import db, User
from passlib.hash import sha256_crypt

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
        global app
        basedir = os.path.abspath(os.path.dirname(__file__))
        app = create_app({
                         'TESTING': True,
                         'ENV': 'test',
                         'SQLALCHEMY_DATABASE_URI': 'sqlite:///' +
                         os.path.join(basedir, TEST_DB),
                         'USERNAME': 'Test',
                         'PASSWORD': 'password123',
                         'debug': True
                         })
        self.app = app.test_client()
        app.app_context().push()
        db.create_all()
        hashed_pass = sha256_crypt.hash(app.config['PASSWORD'])
        user = User(firstname='mock',
                    lastname='mock',
                    username=app.config['USERNAME'],
                    email="mock@gmail.com",
                    password=hashed_pass,
                    terms=True
                    )
        user.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_homepage(self):
        """ test user not connected page """
        request = self.app.get("/")
        self.assertEqual(request.status_code, 200)

    def test_registered_user(self):
        """ tests if user is registered successfully before commiting """
        user = User(firstname="Test", lastname="Lase", username="User",
                    email="Email@gmail.com", password="nvmmme", terms=True)
        db.session.add(user)
        self.assertIn(user, db.session)

    def _login(self, username, password):
        """ login helper function """
        return self.app.post('/auth/login/',
                             data={'username': username,
                                   'password': password},
                             follow_redirects=True,
                             )

    def _logout(self):
        """ logout helper function """
        return self.app.get('/auth/logout/', follow_redirects=True)

    def test_login_logout(self):
        """ test login and logout using helper functions """
        request = self._login(app.config['USERNAME'],
                             app.config['PASSWORD'])
        self.assertIn(b'You are now logged in!', request.data)
        request = self._logout()
        self.assertIn(b'You logged out successfully!', request.data)

    def test_invalid_login(self):
        """ test invalid login using helper function """
        request = self._login(app.config['USERNAME'] + ' Y',
                             app.config['PASSWORD'] + ' Y')
        self.assertIn(b'Check your credentials and try again!', request.data)

    def test_login_required_wrapper(self):
        """ test if the login required wrapper works """
        request = self._logout()
        self.assertIn(b'You need to login first', request.data)

    def test_logout_required_wrapper(self):
        request = self._login(app.config['USERNAME'],
                             app.config['PASSWORD'])
        request = self._login(app.config['USERNAME'],
                             app.config['PASSWORD'])
        self.assertIn(b'You need to logout first.', request.data)


if __name__ == '__main__':
    unittest.main()
