""" Test module"""
import unittest
import json
from app import main


class AppTest(unittest.TestCase):
    """ Test class"""

    def setUp(self):
        self.app = main.create_app()
        self.client = self.app.test_client()
        
    def tearDown(self):
        pass

    #### GLOBAL TEST



if __name__ == '__main__':
    unittest.main()
