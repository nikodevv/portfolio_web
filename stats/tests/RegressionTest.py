from unittest import TestCase as PythonTestCase
from stats.database_tools.Controller import Processor
from stats.tests.test_dataGeneration import TestData
from stats.models import Match

class TestProcessorMakesModels:
	def setUp(self):
		self.processor = Processor()

	def test_can_create_games(self):
		self.assertEqual(Match.objects.all(), [])
		mdetails = TestData.create_match_details_data()
		self.processor.create_game(mdetails)
		self.assertEqual(len(Match.objects.all()), 1)
		self.assertEqual(Match.objects.first().mid, mdetails['match_id'])