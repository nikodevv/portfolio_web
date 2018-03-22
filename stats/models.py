import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from django.db import models
# Create your models here.
class Tournament(models.Model):
	""" 
	Class representing a pro tournament metadata
	"""
	tid = models.CharField(max_length=255, default='novalue')
	tindex = models.CharField(max_length=255, default='novalue')
	tname = models.CharField(max_length=255, default='novalue')

	
class Match(models.Model):
	# ids are CharFields to prevent reading 003 as 3.
	# Foreign Keys
	tournament = models.ForeignKey(Tournament, null=False, blank=True)
	# Game attributes
	mid = models.CharField(primary_key=True, max_length=255) # match id
	mlength = models.CharField(max_length=255) # match length
	win_radiant = models.BooleanField(default=True)
	# Team specific attributes
	rad_teamid = models.CharField(max_length=255, default='novalue')
	dire_teamid = models.CharField(max_length=255, default='novalue')
	rad1_heroid = models.CharField(max_length=10, default='novalue')
	rad2_heroid = models.CharField(max_length=10, default='novalue')
	rad3_heroid = models.CharField(max_length=10, default='novalue')
	rad4_heroid = models.CharField(max_length=10, default='novalue')
	rad5_heroid = models.CharField(max_length=10, default='novalue')
	rad1_playerid = models.CharField(max_length=10, default='novalue')
	rad2_playerid = models.CharField(max_length=10, default='novalue')
	rad3_playerid = models.CharField(max_length=10, default='novalue')
	rad4_playerid = models.CharField(max_length=10, default='novalue')
	rad5_playerid = models.CharField(max_length=10, default='novalue')
	
	# Enemy specifc attirbutes
	dire1_heroid = models.CharField(max_length=10, default='novalue')
	dire2_heroid = models.CharField(max_length=10, default='novalue')
	dire3_heroid = models.CharField(max_length=10, default='novalue')
	dire4_heroid = models.CharField(max_length=10, default='novalue')
	dire5_heroid = models.CharField(max_length=10, default='novalue')
	dire1_playerid = models.CharField(max_length=10, default='novalue')
	dire2_playerid = models.CharField(max_length=10, default='novalue')
	dire3_playerid = models.CharField(max_length=10, default='novalue')
	dire4_playerid = models.CharField(max_length=10, default='novalue')
	dire5_playerid = models.CharField(max_length=10, default='novalue')

class Inventory(models.Model):
	match = models.ForeignKey(Match, related_name="players_inventories")
	