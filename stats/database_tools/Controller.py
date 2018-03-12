import dota2api
import json
from stats import models # might cause issues
from django.db import models
from stats.models import Tournament, Sides, Match

class Controller:
	START_ID = 17411 # using itemdef not id
	END_ID = 25000 # using itemdef not id

	def __init__(self, API_KEY):
		# To-Do: import Models Base Class
		self.api = dota2api.Initialise(API_KEY)
		self.processor = Processor()

	def create_tournaments(self, tournament_data=None):
		# allows unit testing
		if tournament_data == None:
			tournament_data = self.get_tournaments(START, END)

	def get_tournaments(self, start, end):
		"""returns array with tournament metadata"""
		wrapper_leagues = self.api.get_league_listing()
		tournaments = []
		for tourmnt in wrapper_leagues['leagues']:
			if (tourmnt['itemdef'] <= end) and (tourmnt['itemdef'] >= start):
				try:
					tournaments.append({'index': tourmnt['itemdef'], 
						'id': tourmnt['leagueid'], 'name': tourmnt['name']})
				except:
					# Likely Encoding error
					pass
		return tournaments

class Processor:
	""" A data processing layer that passes input to models.Manager """
	def __init__(self):
		t_manager = TournamentManager()
		g_manager = GameManager()

	def create_tournament(tournament_data):
		t_manager.create() # not defined yet

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
	def create(self, match, win_r, rad_teamid, dire_teamid, hero_ids, player_ids):
		self.create_match(match, win_r, rad_teamid, dire_teamid, hero_ids, player_ids)

	@staticmethod
	def create_match(tournament, match_id, win_r, rad_teamid, dire_teamid, hero_ids, player_ids):
		entry = Match()
		entry.match_id = match_id
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

# so now i want to get data not found in match_history and pass it to process

# Foreign Keys
	## match = models.ForeignKey(Match)
	## # Game attributes
	## win_radiant = models.BooleanField(default=True)
	# # Team specific attributes
	## rad_teamid = models.DecimalField(max_digits=3, decimal_places=0)
	## dire_teamid = models.DecimalField(max_digits=3, decimal_places=0)
	## rad1_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	### rad2_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	# rad3_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	# rad4_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	# rad5_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	# rad1_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	# rad2_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	# rad3_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	# rad4_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	# rad5_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	
	# # Enemy specifc attirbutes
	# dire1_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	# dire2_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	# dire3_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	# dire4_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	# dire5_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	# dire1_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	# dire2_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	# dire3_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	# dire4_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	# dire5_playerid = models.DecimalField(max_digits=4, decimal_places=0)