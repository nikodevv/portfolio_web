from django.test import TestCase

# Create your tests here.

class TestViews(TestCase):
	def test_homepage_returns_correct_html(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'homepage.html')

	def test_mobile_homepage_returns_correct_html(self):
		response = self.client.get('/home-mobile/')
		self.assertTemplateUsed(response, 'home-mobile.html')

	def test_contact_page_returns_correct_html(self):
		response = self.client.get('/contact/')
		self.assertTemplateUsed(response,'contact.html')

	def test_mobile_contact_page_returns_correct_html(self):
		response = self.client.get('/contact-mobile/')
		self.assertTemplateUsed(response,'contact-mobile.html')

	def test_resume_page_returns_correct_html(self):
		response = self.client.get('/resume/')
		self.assertTemplateUsed(response,'resume.html')

	def test_toronto_page_returns_correct_html(self):
		response = self.client.get('/projects/toronto_sky/')
		self.assertTemplateUsed(response,'toronto_sky.html')

	def test_projects_page_returns_correct_html(self):
		response = self.client.get('/projects/')
		self.assertTemplateUsed(response,'projects.html')

	def test_urls_are_finished(self):
		self.fail("Remove all stats test from this branch, and clean up URL names"+
			" so that all names use consistent methodology. In particular this means editing the" + 
			" redirection script for mobile.")