from django.test import TestCase

# Create your tests here.

class TestViews(TestCase):
	def test_homepage_returns_correct_html(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'homepage.html')