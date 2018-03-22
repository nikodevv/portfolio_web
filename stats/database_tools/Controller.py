import dota2api
import sys, django
from os.path import dirname, abspath
import os
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_web.settings")
django.setup()
from stats.models import Tournament, Match

class Controller:
	"""
	Makes API calls and dispatches information to be Processed
	"""
	START_ID = 17411 # using itemdef not id
	END_ID = 25000 # using itemdef not id

	def __init__(self, API_KEY):
		self.api = dota2api.Initialise(API_KEY)
		self.processor = Processor(Controller.START_ID, Controller.END_ID)

	def create_tournaments(self):
		"""Collects data from valve API and passes it to processor"""
		# Stores tournament data and stores list of tournament ids
		self.tournament_ids = self.processor.create_tournaments(
			self.get_tournaments(START_ID, END_ID))

	def create_matches(self):
		match_ids = []
		for id_ in self.tournament_ids:
			match_ids.append(self.processor.get_match_ids_from_api_call(
				self.api.get_match_history(league=id_)))
		# Now make it call function that stores match details through processor
		for id_ in match_ids:
			self.processor.create_game(self.get_match_details(id_))

	def get_tournaments(self, start, end):
		return self.api.get_league_listing()['leagues']

	def get_match_details(self, match_id):
		return self.api.get_match_history(match_id)

class Processor:
	""" A data processing layer that takes large dictonaries, and filters 
	the data to models.Managers (models factories) """ 
	def __init__(self, start, end):
		self.t_manager = TournamentManager()
		self.g_manager = GameManager()
		self.START= start
		self.END = end

	def create_tournaments(self, tournament_data):
		tournament_ids = []
		for data in tournament_data:
			if int(data['itemdef']) >= self.START and int(data['itemdef']) <= self.END:
				tournament_ids.append(self.t_manager.create(*self._filter_tdata(data)).tid)
		return tournament_ids

	def create_game(self, mdata):
		"""
		takes a matchdetails dota2api call and dispatches relevant info to
		models manager
		"""
		tournament_id = mdata['leagueid']
		match_id = mdata['match_id']
		win_r = mdata['radiant_win'] # True if radiant won
		rad_teamid = mdata['radiant_team']['team_name'] 
		dire_teamid = mdata['dire_team']['team_name']
		players = self.get_players(mdata['players'])
		heroes = self.get_heroes(mdata['players'])
		self.g_manager.create(tournament_id, match_id, win_r, rad_teamid, 
			dire_teamid, heroes, players)

	@staticmethod
	def _filter_tdata(data):
		return data['leagueid'], data['itemdef'], data['name']

	@staticmethod 
	def get_match_ids_from_api_call(data):
		return [match['match_id'] for match in data['matches']]

	@staticmethod
	def get_heroes(player_data):
		# Can get items by [player['item_3'] for player in player_data]
		# ^ i.e. thats for itemslot 3
		return [player['hero_id'] for player in player_data]

	@staticmethod 
	def get_players(player_data):
		return [player['account_id'] for player in player_data]

class TournamentManager(models.Manager):
	@staticmethod
	def create(tid, tindex, tname):
		entry = Tournament()
		entry.tid = tid
		entry.tindex = tindex
		entry.tname = tname
		entry.save()
		return entry

class GameManager(models.Manager):
	def create(self, tournament_id, match, win_r, rad_teamid, dire_teamid, 
		hero_ids, player_ids):
		self.create_match(tournament_id, match, win_r, rad_teamid, dire_teamid, 
			hero_ids, player_ids)

	@staticmethod
	def create_match(tournament, match_id, win_r, rad_teamid, dire_teamid, 
		hero_ids, player_ids):
		entry = Match()
		entry.mid = match_id
		entry.win_radiant = win_r
		entry.rad_teamid = rad_teamid
		entry.dire_teamid = dire_teamid

		entry.rad1_heroid = hero_ids[0]
		entry.rad2_heroid = hero_ids[1]
		entry.rad3_heroid = hero_ids[2]
		entry.rad4_heroid = hero_ids[3]
		entry.rad5_heroid = hero_ids[4]
		entry.dire1_heroid = hero_ids[5]
		entry.dire2_heroid = hero_ids[6]
		entry.dire3_heroid = hero_ids[7]
		entry.dire4_heroid = hero_ids[8]
		entry.dire5_heroid = hero_ids[9]

		entry.rad1_playerid = player_ids[0]
		entry.rad2_playerid = player_ids[1]
		entry.rad3_playerid = player_ids[2]
		entry.rad4_playerid = player_ids[3]
		entry.rad5_playerid = player_ids[4]
		entry.dire1_playerid = player_ids[5]
		entry.dire2_playerid = player_ids[6]
		entry.dire3_playerid = player_ids[7]
		entry.dire4_playerid = player_ids[8]
		entry.dire5_playerid = player_ids[9]
		entry.save()
API_KEY = '93E37410337F61C24E4C2496BFB68DE0'
models_creator = Controller(API_KEY)