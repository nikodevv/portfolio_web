from django.shortcuts import render

# Create your views here.
def home_view(request):
	return render(request, 'homepage.html', {'current_page': 'About'})

def home_m_view(request):
	# has to return home-mobile.html not hompage-mobile.html, even though
	# the latter would be consistent with home_view()
	# This is because of a front-end redirect script
	return render(request, 'home-mobile.html', {'current_page': 'About'})

def contact_view(request):
	return render(request, 'contact.html', {'current_page': 'Contact'})

def contact_m_view(request):
	return render(request, 'contact-mobile.html', {'current_page': 'Contact'})

def resume_view(request):
	return render(request, 'resume.html', {'current_page': 'Resume'})

def resume_m_view(request):
	return render(request, 'resume-mobile.html', {'current_page': 'Resume'})

def projects_view(request):
	return render(request, 'projects.html', {'current_page': 'Projects'})

def projects_m_view(request):
	return render(request, 'projects-mobile.html', {'current_page': 'Projects'})

# tiny apps that don't warrant their own folder views go below
def toronto_sky_view(request):
	return render(request, 'toronto_sky.html', {'current_page': 'Projects'})

def toronto_sky_m_view(request):
	return render(request, 'toronto_sky-mobile.html', {'current_page': 'Projects'})

def react_test(request):
	return render(request, 'react-app.html')