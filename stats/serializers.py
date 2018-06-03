from rest_framework import serializers
from stats.models import Tournament, Match

class TournamentSerializer(serializers.ModelSerializer):
	# matches stats.models.Tournament fields with corresponding names,
	# effectively filtering them.
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

