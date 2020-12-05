import unittest
import os
import requests

from webapp import app
from bs4 import BeautifulSoup


class FlaskTests(unittest.TestCase):
    def setUp(self):
        os.environ['NO_PROXY'] = '0.0.0.0'
        self.app = app.test_client()

        pass

    def test_homePage(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)