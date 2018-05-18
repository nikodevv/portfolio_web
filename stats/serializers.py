from rest_framework import serializers
from stats.models import Tournament
class TournamentSerializer(serializers.Serializer):
	# matches stats.models.Tournament fields with corresponding names,
	# effectively filtering them.
	class Meta:
		model = Tournament
		fields = ('tid', 'tname')
		# Sets all fields to read-only
		read_only_fields = fields

