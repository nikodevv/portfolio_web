from dota2_api import Initialize
import json

class Controller():
	def __init__(self, API_KEY):
		api = Initialize(API_KEY)
		