from django.shortcuts import render

# Create your views here.
def home_view(request):
	return render(request, 'homepage.html', {'current_page': 'Home'})

def contact_view(request):
	return render(request, 'contact.html', {'current_page': 'Contact'})

def resume_view(request):
	return render(request, 'resume.html', {'current_page': 'Resume'})

def projects_view(request):
	return render(request, 'projects.html', {'current_page': 'Projects'})

# tiny apps that don't warrant their own folder views go below
def toronto_sky_view(request):
	return render(request, 'toronto_sky.html', {'current_page': 'Projects'})

