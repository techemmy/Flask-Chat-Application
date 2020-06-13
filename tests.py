import unittest
from selenium import webdriver
from models import User, Channel, Message, messages_relations, members
from application import app
from flask import session

driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")

class AuthenticationViewTests(unittest.TestCase):
	""" Tests for views of user authentication"""
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

if __name__ == "__main__":
	unittest.main()