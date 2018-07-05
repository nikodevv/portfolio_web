import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from django.db import models
# Create your models here.
class Tournament(models.Model):
	""" 
	Class representing a pdro tournament metadata
	"""
	tid = models.CharField(max_length=255, primary_key=True)
	tindex = models.CharField(max_length=255, default='novalue')
	tname = models.CharField(max_length=255, default='novalue')

	
class Match(models.Model):
	# ids are CharFields to prevent reading 003 as 3.
	# Foreign Keys
	tournament = models.ForeignKey(Tournament, blank=True)
	# Game attributes
	mid = models.CharField(primary_key=True, max_length=255) # match id
	# mlength = models.CharField(max_length=255) # match length
	win_radiant = models.BooleanField(default=True)
	# Team specific attributes
	rad_teamid = models.CharField(max_length=255, default='novalue')
	dire_teamid = models.CharField(max_length=255, default='novalue')

class Player(models.Model):
	"""
	Holds match-specifc player info
	"""
	match = models.ForeignKey(Match, on_delete=models.CASCADE)
	# True or False whether Player is on radiant side.
	rad = models.BooleanField()
	heroid = models.CharField(max_length=255, default='novalue')
	playerid = models.CharField(max_length=255, default='novalue')
	class Meta:
		unique_together = (('match', 'playerid'), ('match', 'heroid'))