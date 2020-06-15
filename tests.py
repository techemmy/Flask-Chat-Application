import unittest
import os
from flask_testing import TestCase
from application import create_app, User
from models import db
from selenium import webdriver



class AuthenticationTests(TestCase):
	""" Tests for views of user authentication"""
	pass

if __name__ == "__main__":
	unittest.main()