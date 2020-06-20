import unittest
from application import create_app


class HookTest(unittest.TestCase):
    """ Test to confirm app works """
    def test_index(self):
	    tester = create_app().test_client()
	    response = tester.get("/", content_type='text/html')
	    self.assertEqual(response.status_code, 200)

class AuthenticationTests(unittest.TestCase):
    """ Test for authentication """
    def setUp(self):
        app = create_app()

if __name__ == '__main__':
    unittest.main()