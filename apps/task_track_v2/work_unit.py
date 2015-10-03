"""
A unit of work (done).

Includes serialization / deserialization to file for single object and collection of objects.
"""

import json
import datetime 
import time
import copy

def dateNow():
	return datetime.datetime.now(datetime.timezone.utc)

def dateNowStr():
	return dateNow().isoformat()

def dateStrToDateTime(d):
	# '2015-10-03T16:15:30.200216+00:00' does not match format 
	# '%Y-%m-%dT%H:%M:%S.%f+%z'
	# ^^ there is an extra ':' in the tz
	assert d[-3] == ':'
	d = d[0:-3] + d[-2:]
	return datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%f%z")

def dateTimeToStr(d):
	return d.isoformat()

class Encoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

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

def toFile(filename, workDoneSet):
	# @@improvement: make file easy to read / modify manually
	# date as localtime with proper ISO8601 encoding
	# endlines between entries

	def dateToStr(w):
		ww = copy.deepcopy(w)
		ww.date = dateTimeToStr(ww.date)
		return ww
	
	workDoneSetWrite = list(map( dateToStr, workDoneSet ))

	encoded = Encoder().encode(workDoneSetWrite)
	open(filename, 'w').write(encoded)

def fromFile(filename):
	"""
	Return: set of WorkDone ordered by chronological time.
	"""

	jl = json.loads( open(filename).read() )
	wd = []
	for item in jl:
		workDone = WorkDone( item['type'], item['length'], item['comment'], dateStrToDateTime(item['date']) )
		wd.append(workDone)
	wd.sort( key= lambda x: x.date )
	return wd

def unitTests():
	filename = 'unit-tests.json'
	wd = []
	
	wd.append( WorkDone('test', 1, 'test item 1',datetime.datetime.fromtimestamp(1443888930.2002168, datetime.timezone.utc) ) )
	wd.append( WorkDone('test', 3.1, 'test\n\n\n item 2', datetime.datetime.fromtimestamp(1443888931.2002168, datetime.timezone.utc)))
	toFile(filename, wd)

	wdRead = fromFile(filename)
	for i in range(len(wd)):
		assert wd[i].type == wdRead[i].type
		assert wd[i].length == wdRead[i].length
		assert wd[i].comment == wdRead[i].comment
		assert wd[i].date == wdRead[i].date
	
	# Test default CTOR / serialization.
	wd.append( WorkDone('test', 1.1, 'test3') )
	toFile(filename, wd)
	wdRead = fromFile(filename)

if __name__ == '__main__':
	#print(dateNowStr())
	unitTests()

