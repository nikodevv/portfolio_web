import dota2api
import json
from stats import models # might cause issues
from django.db import models
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
		self.processor.create_tournaments(self.get_tournaments(START_ID, END_ID), BasicAPI())

	def get_tournaments(self, start, end):
		"""calls api to find necessary tournaments"""
		# for tourmnt in leagues:
		# 	self.processor.create_tournament()
			#if (tourmnt['itemdef'] <= end) and (tourmnt['itemdef'] >= start):

		return self.api.get_league_listing()['leagues']


	def get_match_details(self, match_id):
		#self.api.
		pass

class Processor:
	""" A data processing layer that takes large dictonaries, and filters 
	the data to models.Managers (models factories) """ 
	def __init__(self, start, end):
		self.t_manager = TournamentManager()
		self.g_manager = GameManager()
		self.START= start
		self.END = end

	def create_tournaments(self, tournament_data):
		tournaments = []
		for data in tournament_data:
			if data['itemdef'] >= self.START and data['itemdef'] <= self.END:
				self.t_manager.create(*self._filter_tdata(data))

	@staticmethod
	def _filter_tdata(data):
		return data['leagueid'], data['itemdef'], data['name']

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
	def create(self, tournament, match, win_r, rad_teamid, dire_teamid, 
		hero_ids, player_ids):
		self.create_match(tournament, match, win_r, rad_teamid, dire_teamid, 
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