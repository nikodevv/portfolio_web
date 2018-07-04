from rest_framework import serializers
from stats.models import Tournament, Match, Player

class TournamentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields = ('tid', 'tname')
		read_only_fields = fields

class MatchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Match
		# django > 3.5 requires sepcifing fields = "__all__"
		# otherwise default behaviour is to automatically
		# serialize all fields
		fields = "__all__"

class PlayerSerializers(serializers.ModelSerializer):
	class Meta:
		model = Player
		fields = "__all__"