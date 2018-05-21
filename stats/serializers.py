from rest_framework import serializers
from stats.models import Tournament

class TournamentSerializer(serializers.ModelSerializer):
	# matches stats.models.Tournament fields with corresponding names,
	# effectively filtering them.
	class Meta:
		model = Tournament
		fields = ('tid', 'tname')
		read_only_fields = fields