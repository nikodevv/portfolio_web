from django.shortcuts import render

# Create your views here.
def home_view(request):
	return render(request, 'homepage.html', {'current_page': 'Home'})

def contact_view(request):
	return render(request, 'contact.html', {'current_page': 'Contact'})