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
	Displays list of matches based on query parameters.
	To link together multiple parameters for the same 
	field (i.e. to look up two different team ids),
	seperate parameters with '-'. For example
	./matches?team_id=11111-22222
	"""
	serializer_class = MatchSerializer

	def get_queryset(self):
		"""
		Returns and optionally filters matches 
		against parameters including "team_id"
		"""
		queryset =  Match.objects.all()
		# Is this ok? passing self like that?
		queryset = TeamQueryFilter.filter(self.request, queryset)
		return queryset


class TeamQueryFilter:
	@staticmethod
	def filter(request, queryset):
		team_id = request.query_params.get('team_id', None)
		if team_id is not None:
			team_id = _format_team_id(team_id)
			queryset = _filter_teams(queryset, team_id)
		return queryset

	@staticmethod
	def _filter_teams(queryset, teams):
		# Note time complexity does not include postgreSQL
		# search operations (generally log(n) time).

		# sets queryset to match any games with first team in teams
		final_queryset = _filter_for_team_id(queryset, teams[0])
		# unites querysets for each team to the first
		for team in teams:
			if team is not teams[0]:
				final_queryset = final_queryset.union(
					_filter_for_team_id(queryset, team))
		return final_queryset
	
	@staticmethod
	def _filter_for_team_id(queryset, team_id):
		return queryset.filter(rad_teamid=team_id).union(
			queryset.filter(dire_teamid=team_id))

	@staticmethod
	def _format_team_id(team_ids_string):
		if "-" not in team_ids_string:
			return [team_ids_string]
		return team_ids_string.split("-")