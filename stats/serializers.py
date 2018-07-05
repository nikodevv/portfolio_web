from rest_framework import serializers
from stats.models import Tournament, Match, Player

class TournamentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields = ('tid', 'tname')
		read_only_fields = fields



class PlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Player
		fields = ("rad","heroid","playerid")

class MatchSerializer(serializers.ModelSerializer):
	players = PlayerSerializer(many=True, source='player_set')
	class Meta:
		model = Match
		fields = ("tournament", "mid", "rad_teamid","dire_teamid",
		"win_radiant", "players")