from unittest import TestCase as PythonTestCase
import os, sys
import dota2api
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stats.database_tools.Controller import Controller, Processor 
from stats.models import Tournament

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

class TestProcessor(PythonTestCase):
	def setUp(self):
		START = 17411
		self.processor = Processor(START, 25000)

	def test_tournament_filter(self):
		data = {'name': 'one_name', 'randomename': 'randomVar', 'itemdef':3, 'leagueid':30}
		arg1, arg2, arg3 = self.processor._filter_tdata(data)
		self.assertEqual(arg1, data['leagueid'])
		self.assertEqual(arg2, data['itemdef'])
		self.assertEqual(arg3, data['name'][:20])

	def test_tournament_creation(self):
		data1 = {'name': 'First Name', 'randomename': 'randomVar', 'itemdef':18000, 'leagueid':30}
		# itemdef > the START specified value in setUp(), so data2 should not stored in db
		data2 = {'name': 'Second Name', 'randomename': 'randomVar2', 'itemdef':17000, 'leagueid':34}
		data3 = {'name': 'Second Name', 'randomename': 'randomVar2', 'itemdef':19000, 'leagueid':34}
		data = [data1, data2, data3]
		self.processor.create_tournaments(data)
		tournaments = Tournament.objects.all()
		# creates only 2 tournaments
		self.assertEqual(len(tournaments), 2)
		# tournament 1 is the frsit tournament
		self.assertEqual(tournaments[0].tid,  '30')
		self.assertEqual(tournaments[1].tindex, '19000')