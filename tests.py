import unittest
import os
from flask_testing import TestCase
from application import create_app, User
from models import db
from selenium import webdriver


driver = webdriver.Chrome()

class AuthenticationTests(TestCase):
	""" Tests for views of user authentication"""
	# SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
	# TESTING = True
			
	# def create_app(test_config):
	# 	test_config = {
	# 		'ENV': 'test'
	# 	}
	# 	return create_app(test_config)

	# def setUp(self):
	# 	db.create_all()

	# def tearDown(self):
	# 	db.session.remove()
	# 	db.drop_all()

	def test_user_not_connected_homepage(self):
		driver.get("localhost:5000")
		signup_btn = driver.find_element_by_id("signup_btn")
		login_btn = driver.find_element_by_id("login_btn")
		self.assertEqual(driver.title, "Hook - Connect")
		self.assertEqual(signup_btn.text, "Sign Up")
		self.assertEqual(login_btn.text, "Log In")

	def test_user_login_redirect(self):
		driver.get("localhost:5000/chat")
		message = driver.find_element_by_id("alert-message")
		self.assertEqual(message.text, "You need to login first\n×")

	def test_registered_user(self):
		# user = User.add_user("FirstName", "LastName", "User", "Email@gmail.com", "password123", True)
		# db.session.add(user)
		# assert user in db.session
		pass

if __name__ == "__main__":
	unittest.main()