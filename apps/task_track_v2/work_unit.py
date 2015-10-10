"""
A unit of work (done).
"""

import datetime

import options

def dateNow():
	return datetime.datetime.now(datetime.timezone.utc)

def dateNowStr():
	return dateNow().isoformat()

class WorkDone:
	def __init__(self, typei, length, comment = '', date = dateNow()):
		assert type(typei) == str
		assert type(length) == int or type(length) == float
		assert type(comment) == str
		assert type(date) == datetime.datetime

		self.type = typei
		self.length = length
		self.date = date
		self.comment = comment

