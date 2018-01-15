from django.test import TestCase

# Create your tests here.

class TestViews(TestCase):
	def test_homepage_returns_correct_html(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'homepage.html')

	def test_contact_page_returns_correct_html(self):
		response = self.client.get('/contact/')
		self.assertTemplateUsed(response,'contact.html')
	
	def test_resume_page_returns_correct_html(self):
		response = self.client.get('/resume/')
		self.assertTemplateUsed(response,'resume.html')