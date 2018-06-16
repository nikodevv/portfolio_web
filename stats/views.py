from django.shortcuts import render
from django.db.models import Q
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

# Speed can be improved if reformatted via | instead of union
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
		queryset = HeroQueryFilter.filter(self.request, queryset)
		return queryset


class TeamQueryFilter:
	@staticmethod
	def filter(request, queryset):
		team_id = request.query_params.get('teams', None)
		if team_id is not None:
			# breaks out team_ids string into list
			team_id = team_id.split(",") 
			queryset = TeamQueryFilter._filter_teams(queryset, team_id)
		return queryset

	@staticmethod
	def _filter_teams(queryset, teams):
		# Note time complexity does not include postgreSQL
		# search operations (generally log(n) time).

		# sets queryset to match any games with first team in teams
		if isinstance(teams, list) == True:
			final_queryset = TeamQueryFilter._filter_for_team_id(queryset, teams[0])
		else:
			final_queryset = TeamQueryFilter._filter_for_team_id(queryset, teams)

		# unites querysets for each team to the first
		for team in teams:
			if team is not teams[0]:
				final_queryset = final_queryset.union(
					TeamQueryFilter._filter_for_team_id(queryset, team))
		return final_queryset
	
	#Refactor for Q not union
	@staticmethod
	def _filter_for_team_id(queryset, team_id):
		return queryset.filter(
			Q(rad_teamid=team_id) | Q(dire_teamid=team_id)
			)


class HeroQueryFilter:
	@staticmethod
	def filter(request, queryset):
		hero_ids = request.query_params.get('heroes', None)
		if hero_ids is not None:
			hero_ids = hero_ids.split(",")
			queryset = HeroQueryFilter._filter_heroes(hero_ids, queryset)
		return queryset

	@staticmethod
	def _filter_heroes(hero_ids, queryset):
		# iterates over list if id_ is lists, else just calls function directly
		if isinstance(hero_ids, list) == True:
			final_queryset = HeroQueryFilter._get_relevant_matches(hero_ids[0], queryset)
			for id_ in hero_ids:
				final_queryset = final_queryset | HeroQueryFilter._get_relevant_matches(id_, queryset)
		else:
			final_queryset = HeroQueryFilter._get_relevant_matches(hero_ids, queryset)
		return final_queryset

	@staticmethod
	def _get_relevant_matches(id_, queryset):
		queryset = queryset.filter(
			Q(rad1_heroid=id_) |
			Q(rad2_heroid=id_) |
			Q(rad3_heroid=id_) |
			Q(rad4_heroid=id_) |
			Q(rad5_heroid=id_) |
			Q(dire1_heroid=id_) |
			Q(dire2_heroid=id_) |
			Q(dire3_heroid=id_) |
			Q(dire4_heroid=id_) |
			Q(dire5_heroid=id_) 
			)
		return queryset