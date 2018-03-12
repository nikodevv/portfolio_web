from unittest import TestCase as PythonTestCase
import os, sys
import dota2api
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stats.database_tools.Controller import Controller, Processor 

API_KEY = '93E37410337F61C24E4C2496BFB68DE0'

class TestController(PythonTestCase):
	def setUp(self):
		self.controller = Controller(API_KEY)

	def test_api_is_created(self):
		# using isInstance or assertIsInstance is not preferable due to
		# dota2api's Initialise function.

		# league_id=1 is an invalid id and the api returns the default
		# dictionary (i.e. default)
		default =  ({'status': 1, 'num_results': 0, 'total_results': 0, 
			'results_remaining': 0, 'matches': []})
		self.assertEqual(self.controller.api.get_match_history(league_id=1), default)
