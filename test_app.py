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

    def test_NumberResults(self):
        query = "I'm the best in the world"
        params = {"query": query}
        response = self.app.post('/', data=params)
        pageResponse = BeautifulSoup(response.data, 'html.parser')
        result20 = pageResponse.find(class_="index-20")
        result21 = pageResponse.find(class_="index-21")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(result20), '<th class="index-20">20</th>')
        self.assertIsNone(result21, "Number of results: 20")

    def test_ResultsFor(self):
        query = "I'm the best in the world"
        params = {"query": query}
        response = self.app.post('/', data=params)
        pageResponse = BeautifulSoup(response.data, 'html.parser')
        test = pageResponse.find(class_="Results")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(test), '<h5 class="Results">Results for : {}</h5>'.format(query))

    def test_Results(self):
        query = "I'm the best in the world"
        params = {"query": query}
        msg1 = "Thank you to the Robb Report, The Best of the Best issue, for just naming Trump International Golf Links the Best New Golf Course In World!"
        msg7 = "“If you want the best, you’d better be the best – in all aspects of business.” – Think Like a Billionaire"

        response = self.app.post('/', data=params)
        pageResponse = BeautifulSoup(response.data, 'html.parser')
        result1 = pageResponse.find(class_="msg-1")
        result7 = pageResponse.find(class_="msg-7")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(result1), '<td class="msg-1">{}</td>'.format(msg1))
        self.assertEqual(str(result7), '<td class="msg-7">{}</td>'.format(msg7))