from unittest import TestCase as PythonTestCase
from unittest.mock import patch 
import dota2api
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stats.database_tools.Controller import Controller, Processor, GameManager
from stats.models import Tournament

API_KEY = '93E37410337F61C24E4C2496BFB68DE0'

class TestData:
	"""Provides testcases with input data. 
	Naming conventions: t1, t2 ,t3 corresponds to tournament1, tournament2, ..."""
	@staticmethod
	def get_api_data_3_tournaments():
		t1 = TestData.get_api_t1()
		# itemdef > the START specified value in setUp(), so data2 should not stored in db
		t2 = TestData.get_api_t2()
		t3 = TestData.get_api_t3()
		return [t1, t2, t3]
	@staticmethod
	def get_api_t1():
		return {'name': 'First Name', 'randomename': 'randomVar', 'itemdef':'18000', 'leagueid':'30'}
	@staticmethod
	def get_api_t2():
		return {'name': 'Second Name', 'randomename': 'randomVar2', 'itemdef':'17000', 'leagueid':'34'}
	@staticmethod
	def get_api_t3():
		return {'name': 'Second Name', 'randomename': 'randomVar2', 'itemdef':'19000', 'leagueid':'37'}

	@staticmethod
	def get_match_history():
		return ({'status': 1, 'num_results': '', 'total_results': '', 'results_remaining':'',
		'matches': [TestData.get_match1(), TestData.get_match2()]})
	@staticmethod 
	def get_match1():
		return ({'series_id': 1, 'match_id': '40','several_other_keys': 'whatever'})
	@staticmethod
	def get_match2():
		return ({'series_id': 1, 'match_id': '77','several_other_keys': 'whatever'})
	
	@staticmethod
	def create_match_details_data():
		t1 = {'team_name':'Evil Geniuses'}
		t2 = {'team_name':'VGJ'}
		players = TestData.create_10_players()
		return {'leagueid': '3', 'match_id': '10', 'radiant_win': True, 'radiant_team': t1,
		'dire_team':t2, 'players': players}

	@staticmethod
	def create_player_instance(account_number, hero_id):
		return {'account_id': account_number, 'hero_id':hero_id}

	@staticmethod
	def create_10_players():
		return [TestData.create_player_instance(str(x), str(2*x)) for x in range(1, 10)]

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

class TestProcessor(PythonTestCase, TestData):
	def setUp(self):
		START = 17411
		self.processor = Processor(START, 25000)

	def test_tournament_filter(self):
		data = self.get_api_t1()
		arg1, arg2, arg3 = self.processor._filter_tdata(data)
		self.assertEqual(arg1, data['leagueid'])
		self.assertEqual(arg2, data['itemdef'])
		self.assertEqual(arg3, data['name'][:20])

	def test_can_create_tournaments_given_api_input(self):
		data = self.get_api_data_3_tournaments()
		self.processor.create_tournaments(data)
		tournaments = Tournament.objects.all()
		# creates only 2 tournaments due to START = 17411
		self.assertEqual(len(tournaments), 2)
		# tournament 1 is the first tournament
		self.assertEqual(tournaments[0].tid,  data[0]['leagueid'])
		self.assertEqual(tournaments[1].tindex, data[2]['itemdef'])

	def test_tournament_creation_also_returns_tournament_ids_of_created_objects(self):
		data = self.get_api_data_3_tournaments()
		tournament_ids = self.processor.create_tournaments(data)
		self.assertIsInstance(tournament_ids, list)
		# only gets 2 ids back due to START = 17411
		self.assertEqual(tournament_ids, [data[0]['leagueid'], data[2]['leagueid']])

	def test_returns_match_ids(self):
		data = self.get_match_history()
		match_ids = self.processor.get_match_ids_from_api_call(data)
		self.assertEqual(match_ids, [x['match_id'] for x in data['matches']])

	# Processor().create_game(...) should call GameManager.create()
	# The test checks to see if the data is passed to GameManager and if it 
	# is passed in the right order
	# The patch statement replaces the GameManager object name, allowing for
	# to check if a method was called without overwriting it.
	def test_create_game_method_calls_model_manager_equivalent(self):
		mdata = TestData.create_match_details_data()
		heroes_data = Processor.get_heroes(mdata['players'])
		players_data = Processor.get_players(mdata['players'])
		with patch.object(self.processor.g_manager, 'create') as mock:
			self.processor.create_game(mdata)
			mock.assert_called_with(mdata['leagueid'], mdata['match_id'], 
				mdata['radiant_win'], mdata['radiant_team']['team_name'], 
				mdata['dire_team']['team_name'], heroes_data, players_data)

	def test_get_players(self):
		players_data = TestData.create_10_players()
		self.assertEqual(self.processor.get_players(players_data), 
			[player['account_id'] for player in players_data])

	def test_get_heroes(self):
		heroes = TestData.create_10_players()
		self.assertEqual(self.processor.get_heroes(heroes), 
			[player['hero_id'] for player in heroes])
