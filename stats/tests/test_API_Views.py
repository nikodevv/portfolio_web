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

	def test_can_filter_based_on_multiple_match_ids(self):
		self.testData.create_row() #1st has teams [11,22]
		self.testData.create_row(teams=['22','33']) #2nd
		self.testData.create_row(teams=['77','11']) #3rd
		self.testData.create_row(teams=['33','77']) #4th
		self.testData.create_row(teams=['99','33']) #5th
		
		# makes sure all matches are saved to db
		response = self.client.get(self.mURL, format='json')
		data = json.loads(self.decode(response))
		self.assertEqual(len(data),5)

		# sends request filtering for 1st 3rd 4th games
		response = self.client.get(self.mURL + '?teams=11,77', format='json')
		data = json.loads(self.decode(response))
		self.assertEqual(len(data), 3)
		match_ids = self._get_list(data, "mid")
		self.assertIn("1100.0", match_ids)
		self.assertIn("1102.0", match_ids)
		self.assertIn("1103.0", match_ids)
		self.assertNotIn("1101.0", match_ids)


	def test_can_filter_based_on_single_heroid(self):
		#1st has heroes "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
		self.testData.create_row()
		self.testData.create_row(
			heroes = ["22", "2", "33", "4", "5", "6", "7", "8", "9", "11"]
			)
		self.testData.create_row(
			heroes = ["1", "11", "3", "4", "5", "6", "7", "8", "9", "10"]
			)

		# tests that only game 2 and 3 come up when filtering for heroid "11"
		response = self.client.get(self.mURL+"?heroes=11", format='json')
		data = json.loads(self.decode(response))
		self.assertEqual(len(data),2)
		self.assertEqual(data[0]["mid"], "1101.0")
		self.assertEqual(data[1]["mid"], "1102.0")

		# tests that both game 1 and 3 come up when filtering for "3"
		response = self.client.get(self.mURL+"?heroes=3", format='json')
		data = json.loads(self.decode(response))
		self.assertEqual(len(data),2)
		match_ids = self._get_list(data, "mid")
		self.assertIn("1100.0", match_ids)
		self.assertIn("1102.0", match_ids)

	def test_can_filter_based_on_multiple_heroids(self):
		#1st has heroes "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
		self.testData.create_row()
		self.testData.create_row(
			heroes = ["22", "2", "33", "4", "5", "6", "7", "8", "9", "11"]
			)
		self.testData.create_row(
			heroes = ["1", "11", "3", "4", "5", "6", "7", "88", "9", "10"]
			)

		# tests that both game 2 and 3 come up when filtering for "88,22"
		response = self.client.get(self.mURL+"?heroes=88,22", format='json')
		data = json.loads(self.decode(response))
		self.assertEqual(len(data),2)
		match_ids = self._get_list(data, "mid")
		self.assertIn("1101.0", match_ids)
		self.assertIn("1102.0", match_ids)

	def test_hero_and_team_filters_are_applied_on_top_of_eachother(self):
		"""
		tests that filtering for teams=11,3 heroes=12 only returns results where
		teams 11 or 3 picked hero 12, not all games where team 11 or 3 played and all games
		where hero 12 was picked.
		"""
		# by default has heroes = [1, 2, 3, ... 10]
		self.testData.create_row(
			teams = ["999", "888"],
		)
		self.testData.create_row()
		self.testData.create_row(
			teams = ["777", "333"],
		)
		self.testData.create_row(
			teams = ["777", "888"],
			heroes = ["99", "11", "3", "4", "5", "6", "7", "88", "9", "10"]
		)
		# tests that only game 1 and 3 is returned
		response = self.client.get(self.mURL+"?teams=777,999&heroes=1", format='json')
		data = json.loads(self.decode(response))
		self.assertEqual(len(data), 2)
		match_ids = self._get_list(data, "mid")
		self.assertIn("1100.0", match_ids)
		self.assertIn("1102.0", match_ids)
		self.assertNotIn("1103.0", match_ids)

	def decode(self, response):
		return response.content.decode("utf-8", "strict")

	def _get_list(self, data, param):
		""""
		returns list of values from a list of dictionaries such
		that dict[param] is in the returned list for every dict.
		"""
		list_ = []
		for i in data:
			list_.append(i[param])
		return list_

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
			dire_teamid, heroes, self.default_players]

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