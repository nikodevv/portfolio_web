from unittest import TestCase as PythonTestCase
from django.test import TestCase as DjangoTestCase
from unittest.mock import patch 
import dota2api
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stats.database_tools.Controller import Processor, GameManager
from stats.models import Tournament
from stats.tests.timer import TimeIt

class TestGameManager(DjangoTestCase):
	def setUp(self):
		self.g_manager = GameManager()
	
	@TimeIt.executionTime
	def test_create_method_calls_create_game_with_correct_fields(self):
		self.fail("finish test")

	@TimeIt.executionTime
	def test_finds_tournament_instance(self):
		tournament_id = "1"
		entry = Tournament()
		entry.tid = tournament_id
		# tindex can be larger than required
		entry.tindex = 2
		entry.tname = "Sample Tournament"
		entry.save()
		# the value found by GameManager
		val = self.g_manager.get_tournament_by_id(tournament_id)
		self.assertEqual(entry, val)

	@TimeIt.executionTime
	def test_sets_match_length(self):
		self.fail("finish test, implement functionality")

