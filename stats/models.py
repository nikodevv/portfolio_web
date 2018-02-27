from django.db import models

# Create your models here.
class Tournament(models.Model):
	""" 
	Class representing a pro tournament metadata
	"""
	# tournament id
	tid = models.DecimalField(max_digits=11, decimal_places=0, primary_key=True )
	tindex = models.DecimalField(max_digits=11, decimal_places=0)
	tname = models.CharField(max_length=30)

class Match(models.Model):
	mid = models.DecimalField(max_digits=11, decimal_places=0) # match id
	mlength = models.DecimalField(max_digits=11, decimal_places=0) # match length
	tournament = models.ForeignKey(Tournament)
	
class Sides(models.Model):
	# Foreign Keys
	match = models.ForeignKey(Match)
	# Game attributes
	win_radiant = models.BooleanField(default=True)
	# Team specific attributes
	rad1_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	rad2_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	rad3_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	rad4_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	rad5_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	rad1_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	rad2_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	rad3_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	rad4_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	rad5_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	
	# Enemy specifc attirbutes
	dire1_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	dire2_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	dire3_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	dire4_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	dire5_heroid = models.DecimalField(max_digits=3, decimal_places=0)
	dire1_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	dire2_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	dire3_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	dire4_playerid = models.DecimalField(max_digits=4, decimal_places=0)
	dire5_playerid = models.DecimalField(max_digits=4, decimal_places=0)

class Inventory(models.Model):
	match = models.ForeignKey(Match, related_name="players_inventories")
	