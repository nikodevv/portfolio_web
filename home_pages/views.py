from django.shortcuts import render

# Create your views here.
def home_view(request):
	print("view called")
	return render(request, 'homepage.html')