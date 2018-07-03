"""
A collection of utilities for the processing of Valve API data
"""
from django.db import IntegrityError
from time import time, ctime
import pickle

def ignore_duplicate_data_error(fn):
	"""
	Decorator that prevents IntegrityError[s] causing 
	crashes during model validation.
	"""
	def get_args_dict(*args, **kwargs):
		"""
		Serializes an arbitrary number of kwargs into a str
		"""
		# utf-8 will have issues with valve api
		return pickle.dumps(kwargs).decode('utf-16')

	def wrapper(*args, **kwargs):
		try:
			fn(*args)
		except IntegrityError as e:
			log_str = (ctime(time()) + 
				" - prevented IntegrityError crash by call " + fn.__name__ + 
				": Duplicate data. Data not saved to database." + 
				"\r\narguments:::: " + get_args_dict(kwargs))
			add_to_log(log_str)
	return wrapper

def add_to_log(data):
		with open('errorLog.txt', 'ab') as log:
			# Python automatically uses correct line endings
			# to insert new line via \n
			log.write(('\r\n%s' % data).encode())