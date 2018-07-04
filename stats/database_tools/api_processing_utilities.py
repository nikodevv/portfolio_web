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

	def wrapper(*args, **kwargs):
		try:
			fn(*args)
		except IntegrityError:
			log_str = (ctime(time()) + 
				" - prevented IntegrityError crash by call to " + fn.__name__ + 
				": Duplicate data. Data not saved to database." + 
				"\r\narguments:::: " + get_args_dict(kwargs))
			add_to_log(log_str)
	return wrapper

def safe_dict_lookup(fn):
	"""
	Decorator which attempts to execute fn and safely returns
	None if KeyError error occurs
	"""
	def wrapper(*args, **kwargs):
		try:
			return fn(*args)
		except KeyError:
			log_str = (ctime(time()) + 
				" - prevented KeyError crash by call to" + fn.__name__ + 
				"\r\narguments:::: " + get_args_dict(kwargs))
			add_to_log(log_str)
			return None
	return wrapper

def add_to_log(data):
		with open('errorLog.txt', 'ab') as log:
			# Python automatically uses correct line endings
			# to insert new line via \n
			log.write(('\r\n%s' % data).encode())

def get_args_dict(*args, **kwargs):
	"""
	Serializes an arbitrary number of kwargs into a str
	"""
	# utf-8 will have issues with valve api
	return pickle.dumps(kwargs).decode('utf-16')
