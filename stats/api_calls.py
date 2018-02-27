import dota2api
import json
import os
from django.core.management.base import BaseCommand, CommandError
from stats.models import Tournament, Match, Sides, Inventory


API_KEY = '93E37410337F61C24E4C2496BFB68DE0'
api = dota2api.Initialise(API_KEY)

class SaveTournaments():
	def __init__(self, api, start=17411, end=20000):

		self.data_file = self.os.path.join(
			os.path.dirname(os.path.realpath(__file__)), os.path.relpath('data/tournament_ids.json'))
		self.save_data(api, start, end)

	def save_data(self, api, start, end):
		"""Saves the x'th to the y'th tournament metadata"""
		with open(self.data_file, 'w') as file:
			file.write(self.get_data(api, start, end))

	def get_data(self, api, start, end):
		"""returns array with tournament metadata"""
		wrapper_leagues = api.get_league_listing()
		tournaments = []
		for tourmnt in wrapper_leagues['leagues']:
			if (tourmnt['itemdef'] <= end) and (tourmnt['itemdef'] >= start):
				try:
					tournaments.append({'index': tourmnt['itemdef'], 'id': tourmnt['leagueid'], 'name': tourmnt['name']})
				except:
					# Most likely encoding error
					pass
		return json.dumps(tournaments)

def get_matches():
	return [api.get_match_history(league_id=tournament['id']) for tournament in get_saved_tournaments()]

def get_saved_tournaments():
	x = None
	with open(rel_data_path,'r') as file:
		x = file.read()
	return json.loads(x)

class InsertData():
	def __init__(self):
		self.tournaments = get_saved_tournaments()
		self.main()
	def main(self):
		for tournament in self.tournaments:
			for row in api.get_match_history(league_id=tournament['id']):
				self.make_t_data(row)
	def set_t_data(self,row):
		tournament = Tournament()
		tournament.tindex = row['index']
		tournament.tid = row['id']
		tournament.tname = row['name']
		return tournament

	def make_t_data(self, row):
		tournament = self.set_t_data(row)
		tournament.save()
		# self.make_match_data(tournament)

	def set_m_data(self, row, tournament):
		match = Match()
		match.tournament = tournament
		match.length = Null
	def make_match_data(self, tournament):
		pass

insert = InsertData()

class Command(BaseCommand)