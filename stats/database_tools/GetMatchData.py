import dota2api
import sys, django
from os.path import dirname, abspath
from os import environ
from stats.models import Tournament, Match, Player
from django.db import models, IntegrityError
import pickle
from time import time as timestamp
from api_processing_utilities import ignore_duplicate_data_error

# Necesary for django ORM to be used inside a standalone script. 
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_web.settings")
django.setup()


class Controller:
	"""
	Makes API calls and dispatches information to be Processed
	"""

	def __init__(self, API_KEY):
		# Initializing with start @ 17410-17414, 17415-17418, then 17420-17430, finally 17430-17450
		self.START_ID = 17410 # using itemdef not id [prev 17430]
		self.END_ID = 17417 # using itemdef not id #previously 17450
		self.api = dota2api.Initialise(API_KEY)
		self.processor = Processor(self.START_ID, self.END_ID)
		self.create_tournaments()
		self.create_matches()

	def create_tournaments(self):
		"""Collects data from valve API and passes it to processor"""
		# Stores tournament data and stores list of tournament ids
		self.tournament_ids = self.processor.create_tournaments(
			self.get_tournaments(self.START_ID, self.END_ID))

	def create_matches(self):
		match_ids = []
		for id_ in self.tournament_ids:
			# Add in a dictionary for this that holds tid: match_ids
			match_ids = match_ids + (self.processor.get_match_ids_from_api_call(
				self.api.get_match_history(league_id=id_)))
		# call function that stores match details through processor
		for id_ in match_ids:
			self.processor.create_game(self.get_match_details(id_))

	def get_tournaments(self, start, end):
		return self.api.get_league_listing()['leagues']

	def get_match_details(self, match_id):
		return self.api.get_match_details(match_id=match_id)

# Tightly coupled to dota2api.
class Processor:
	"""
	A data processing layer that takes large dictonaries of match 
	data, and passes it to models.Managers after processing.
	""" 
	def __init__(self, start, end):
		self.t_manager = TournamentManager()
		self.g_manager = GameManager()
		self.p_manager = PlayerManager()
		# start and end indicies used to prevent processing
		# duplicate data (which will not pass vailidation
		# tests in models anyway).
		self.START= start 
		self.END = end 

	def create_tournaments(self, tournament_data):
		"""
		Returns a list of tournament ids after creating corresponding
		entries in the database
		"""
		tournament_ids = []
		for data in tournament_data:
			if int(data['itemdef']) >= self.START and int(data['itemdef']) <= self.END:
				tournament_ids.append(self.t_manager.create(*self.__filter_tdata(data)).tid)
		return tournament_ids

	def __filter_tdata(self, data):
		return data['leagueid'], data['itemdef'], data['name']

	def create_game(self, mdata):
		"""
		Takes a dict of match data and passes it for further
		processing if the data is valid.
		"""
		# 2 is game mode for capitins mode

		# create_game_if_game_mode_valid returns an empty function
		# if data is non-valid
		make_game_if_valid_data = self.get_game_making_function(mdata)
		make_game_if_valid_data(mdata)

	def get_game_making_function(self, mdata):
		"""
		Returns reference to a function that passes
		data to GameManager only if data is valid.
		"""
		try:
			# 2 is game mode for capitins mode
			if int(mdata['game_mode']) == int(2):
				return self.pass_data
		except:
			print("OK")
			self.__add_to_log(mdata)
			return (lambda x: x)

	def pass_data(self, mdata):
		matchData = MatchFilter(mdata)
		tournament_id = matchData.get_tournament_id()
		self.__validate_not_null(tournament_id, "tournament_id")
		
		match_id = matchData.get_match_id()
		win_r = matchData.get_winner() # True if radiant won
		rad_teamid, dire_teamid = matchData.get_team_ids()
		players = matchData.get_players()
		heroes = matchData.get_heroes()
		self.g_manager.create(tournament_id, match_id, win_r, rad_teamid, 
			dire_teamid)
		# passes player data to PlayerManager
		for i in range(0, 10):
			rad = True
			if i >= 5:
				rad = False
			self.p_manager.create(players[i], heroes[i], rad, match_id)
			i += i

	def __validate_not_null(self, data, dataname):
		"""
		Checks data is not null without relying on database level
		validation
		"""
		if data == None:
			__add_to_log({"Data Error":
				"No valid tournament_id found in match", 
				"match_data": data['match_id']})
			raise Exception(data is not None, "%s is null" % dataname)

	def __add_to_log(self, data):
		with open('errorLog.txt', 'a') as log:
			# Python automatically uses correct line endings
			# to insert new line via \n
			log.write('\n%s\n' % timestamp())
			pickle.dump(data, log)


	def get_match_ids_from_api_call(self, data):
		return [match['match_id'] for match in data['matches']]

class FieldValidator:
	def _get_field_data(self, data):
		"""
		takes a string and returns one 
		of the appropriate length
		"""
		data = str(data)
		if len(data) >= 255:
			return data[:254]
		return data

# Make field validator function belong to 
# Tournament manager, remove inheritance in other
# managers.
class TournamentManager(models.Manager, FieldValidator):
	def create(self, tid, tindex, tname):
		entry = Tournament()
		entry.tid = tid
		# tindex can be larger than required
		entry.tindex = self._get_field_data(tindex)
		entry.tname = self._get_field_data(tname)
		entry.save()
		return entry


class MatchFilter:
	"""
	Returns models-compliant match data for the requested
	data_type.
	"""
	def __init__(self, mdata):
		self.mdata = mdata

	def get_heroes(self):
		player_data = self.mdata['players']
		return [player['hero_id'] for player in player_data]

	def get_players(self):	
		player_data = self.mdata['players']
		return [player['account_id'] for player in player_data]

	def get_team_ids(self):
		"""
		Finds and returns team ids from valve API match_detail call. 
		"""
		# Sometimes team_ids are not recorded. 
		# i.e. the key 'radiant_team_id' is not in mdata.
		# In such cases default values of 1 or 2 are assigned 
		try:
			radiant = self.mdata['radiant_team_id']
		except:
			__add_to_log({"Data Error": "No radiant team id for match", 
				"match_data": self.mdata})
			radiant = "1"
		try:
			dire = self.mdata['dire_team_id']
		except:
			__add_to_log({"Data Error": "No dire team id for match", 
				"match_data": self.mdata})
			dire = "2"
		return radiant, dire

	def get_tournament_id(self):
		return self.mdata['leagueid']

	def get_winner(self):
		return self.mdata['radiant_win']

	def get_match_id(self):
		return self.mdata['match_id']

class GameManager(models.Manager, FieldValidator):
	def create(self, tournament_id, match, win_r, rad_teamid, dire_teamid):
		tournament = self.get_tournament_by_id(tournament_id)
		try:
			self.create_match(tournament, match, win_r, rad_teamid, dire_teamid)
		except Exception as e:
			print("Error creating game for match id " + str(match))
			print("corresponding to tournament " + str(tournament_id))
			print (e.args)
	
	def create_match(self,tournament, match_id, win_r, rad_teamid, dire_teamid):
		entry = Match()
		entry.tournament = tournament
		entry.mid = self._get_field_data(match_id)
		entry.win_radiant = win_r
		entry.rad_teamid = rad_teamid
		entry.dire_teamid = dire_teamid
		entry.save()

	def get_tournament_by_id(self, tournament_id):
		return Tournament.objects.get(pk=tournament_id)

class PlayerManager(models.Manager, FieldValidator):
	def create(self, player_id, hero_id, rad, match_id):
		entry = Player()
		entry.match = self.get_match_by_id(match_id)
		# True or False whether Player is on radiant side.
		entry.rad = rad
		entry.heroid = hero_id
		entry.playerid = player_id
		self.__safe_save(entry)

	def get_match_by_id(self, id_):
		return Match.objects.get(pk=id_)

	# wrapped to skip over duplicate data instead of crash
	@ignore_duplicate_data_error
	def __safe_save(self, entry):
		entry.save()


API_KEY = '93E37410337F61C24E4C2496BFB68DE0'

if __name__ == '__main__':
	models_creator = Controller(API_KEY)

