from django.test import TestCase as DjangoTestCase
from stats.models import Tournament, Match
from stats.database_tools.Controller import TournamentManager, GameManager
# Create your tests here.

class TestModels(DjangoTestCase):
	def test_saves_tournaments(self):
		pass
	def test_saves_match(self):
		pass
	def test_saves_player_instance(self):
		pass
	def test_cannot_save_incomplete_player_instance(self):
		pass

class TestTournamentManager(DjangoTestCase):
	def setUp(self):
		self.manager = TournamentManager()

	def test_creates_tournament(self):
		tid = '1337'
		tindex = '33'
		tname = 'test Name One 1'
		self.manager.create_tournament(tid=tid, tindex=tindex, tname=tname)
		saved_tournaments = Tournament.objects.all()
		self.assertEqual(saved_tournaments[0].tid, tid)
		self.assertEqual(saved_tournaments[0].tindex, tindex)
		self.assertEqual(saved_tournaments[0].tname, tname)

class TestGameManager(DjangoTestCase):
	def setUp(self):
		self.manager = GameManager()

	def test_creates_matches(self):
		tournament = TournamentManager.create_tournament(tid='9999', 
			tindex='5546', tname='tournament')
		match_id = '1'
		win_radiant = True
		rad_teamid = '3000'
		dire_teamid = '4000'
		player_ids = ['111', '222', '333', '444', '555', '666', '777', '999', '000']
		hero_ids = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
		self.manager.create(tournament, match_id, win_radiant, rad_teamid, dire_teamid, 
			hero_ids, player_ids)
		saved_matches = Match.objects.all()
		self.assertEqual(saved_matches[0].match_id, match_id)
		self.assertEqual(saved_matches[0].win_r, win_radiant)
		self.assertEqual(saved_matches[0].rad_teamid, rad_teamid)
		self.assertEqual(saved_matches[0].rad3_playerid, player_ids[2])
		self.assertEqual(saved_matches[0].dire1_playerid, player_ids[5])
		self.assertEqual(saved_matches[0].rad5_heroid, hero_ids[4])
		self.assertEqual(saved_matches[0].dire5_heroid, hero_ids[9])