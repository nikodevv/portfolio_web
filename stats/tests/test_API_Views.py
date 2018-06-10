from django.test import TestCase
from stats.models import Match, Tournament
from stats.database_tools.Controller import TournamentManager, GameManager
from rest_framework.test import APIClient
import json
# Create your tests here.

class TestMatchList(TestCase):
	def setUp(self):
		self.testData = TestData()
		# makes requests to API
		self.client = APIClient()
		# url for matches
		self.mURL = '/stats/matches'

	def test_can_make_non_filtered_query(self):
		# tests empty database returns '[]' str 
		response = self.client.get(self.mURL,format='json')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.decode(response), "[]")

		# tests that non-empty database also returns 
		# valid response
		self.testData.create_row()
		response = self.client.get(self.mURL,format='json')
		data = json.loads(self.decode(response))
		self.assertEqual(len(data), 1)
		self.testData.create_row()
		self.testData.create_row()
		response = self.client.get(self.mURL,format='json')
		data = json.loads(self.decode(response))		
		self.assertEqual(len(data), 3)
		self.assertEqual(data[0]["mid"], "1100.0")
		self.assertEqual(data[1]["mid"], "1101.0")
		self.assertEqual(data[2]["mid"], "1102.0")

	def test_can_filter_based_on_single_match_id(self):
		self.testData.create_row() #1st has teams [11,22]
		self.testData.create_row(teams=['22','33']) #2nd
		self.testData.create_row(teams=['11','77']) #3rd
		# makes sure all matches are saved to db
		response = self.client.get(self.mURL,format='json')
		data = json.loads(self.decode(response))
		self.assertEqual(len(data),3)

		# sends request filtering for 3rd game
		response = self.client.get(self.mURL + '?teams=77',format='json')
		data = json.loads(self.decode(response))
		self.assertEqual(len(data), 1)
		self.assertEqual(data[0]["mid"], "1102.0")

		# sends request filtering for 1st and 3rd games
		response = self.client.get(self.mURL + '?teams=11',format='json')
		data = json.loads(self.decode(response))
		self.assertEqual(len(data),2)
		self.assertEqual(data[0]["mid"], "1100.0")
		self.assertEqual(data[1]["mid"], "1102.0")

	def decode(self, response):
		return response.content.decode("utf-8", "strict")

class TestData:
	def __init__(self):
		self.tournamentManager = TournamentManager()
		self.gameManager = GameManager()
		self.last_tid = 100
		self.default_teams = ["11", "22"]
		self.default_heroes = [
			"1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
		]
		self.default_players = [
			"11", "22", "33", "44", "55", "66", "77", "88", "99", "00"
		]

	def create_row(self, teams = None, heroes = None):
		"""
		Generates rows of test data in Match and Tournament 
		tables of database. 
		"""
		teams = self._set_None_paramaters_to_class_default('teams', teams)
		heroes = self._set_None_paramaters_to_class_default('heroes', heroes)
		last_tour = Tournament.objects.last()
		tour_params = self.get_next_tour(last_tour)
		last_tour = self.tournamentManager.create(
			tour_params[0], tour_params[1], tour_params[2])
		match_params = self.get_next_match(teams, heroes)
		self.gameManager.create(last_tour.tid, match_params[0], match_params[1], match_params[2], 
			match_params[3], match_params[4], match_params[5])

	def get_next_tour(self, tour):
		"""
		Returns a generated list of all parameters needed by 
		TournamentManger to create Tournament objects. 
		"""
		if tour == None:
			return self.default_tour()
		self.last_tid = str(float(tour.tid) + 1)
		tindex = str(float(tour.tindex) + 1)
		tname = "Tournament # " + tindex
		return [self.last_tid, tindex, tname]

	def default_tour(self):
		return str(self.last_tid), "1000", "Tournament # 1000"

	def get_next_match(self, teams, heroes):
		"""
		returns a list containing all parmaters for creating a
		that need to be passed to a GameManager to create a Match
		object, with the exception of a Tournament object.
		"""
		match_id = str(float(self.last_tid) + 1000)
		win_r = "t"
		rad_teamid = teams[0]
		dire_teamid = teams[1]
		return [match_id, win_r, rad_teamid, 
			dire_teamid, self.default_heroes, self.default_players]

	def _set_None_paramaters_to_class_default(self, param_str, param):
		"""
		Checks if passed a paramater with value of None, 
		will return a class default list. 
		"""
		if param == None:
			if param_str == 'teams':
				param = self.default_teams
			elif param_str == 'heroes':
				param = self.default_heroes
		return param