from django.shortcuts import render
from stats.models import Tournament, Match
from stats.serializers import TournamentSerializer, MatchSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
import json

# Create your views here.

def team_query(request, teams):
	# items = list(testGames.objects.values_list('text').values('text'))
	# items = json.dumps(items)
	return render(request, 'stats_h.html',{'teams':'team_query with params %s' %teams})

def team_tour_query(request, teams, tournaments):

	return render(request, 'stats_h.html',{'teams':'tournament quert with params %s' % teams})

class TournamentList(APIView):
	"""
	Lists all tournaments in database.
	"""
	queryset = Tournament.objects.all()
	def get(self, request, format=None):
		tours = Tournament.objects.all()
		serializer = TournamentSerializer(tours, many=True)
		return Response(serializer.data)

class MatchList(ListAPIView):
	"""
	Displays list of matches based on query parameters
	"""
	serializer_class = MatchSerializer

	def get_queryset(self):
		"""
		Returns and optionally filters matches 
		against parameters including "team_id"
		"""
		queryset =  Match.objects.all()
		team_id = self.request.query_params.get('team_id', None)
		if team_id is not None:
			queryset = queryset.filter(rad_teamid=team_id)
		return queryset