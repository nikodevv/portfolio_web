from django.shortcuts import render
import json

# Create your views here.

def test_view(request):
	# items = list(testGames.objects.values_list('text').values('text'))
	# items = json.dumps(items)
	return render(request, 'stats_h.html')

