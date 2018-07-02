"""
A collection of utilities for the processing of Valve API data
"""
from django.db import IntegrityError

def ignore_duplicate_data_error(fn):
	"""
	Decorator that prevents IntegrityError[s] causing 
	crashes during model validation.
	"""
	def wrapper(*args):
		try:
			fn(*args)
		except IntegrityError:
			print("IntegrityError: Duplicate data. Data not saved to database")
	return wrapper