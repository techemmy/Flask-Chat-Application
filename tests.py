import unittest
from selenium import webdriver
from models import User, Channel, Message, messages_relations, members

# driver = webdriver.Chrome()

class AuthenticationTests(unittest.TestCase):
	""" Tests for user authentication"""
	def test_register_user(self):
		pass

if __name__ == "__main__":
	unittest.main()