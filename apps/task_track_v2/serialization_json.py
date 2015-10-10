"""
Serializes / deserializes the basic class that represent a unit of work done.

It should not have functionality besides reading / writing a set of that class to / from a file.
"""

import json
import datetime 
import time
import copy
import os

import options
from work_unit import WorkDone as WorkDone

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

def toFile(filename, workDoneSet):
	# @@@bug: do not rewrite all file (do not want to delete extra data put manually into tasks).
	# @@improvement: make file easy to read / modify manually
	# date as localtime with proper ISO8601 encoding
	# endlines between entries

	def dateToStr(w):
		ww = copy.deepcopy(w)
		ww.date = dateTimeToStr(ww.date)
		return ww
	
	workDoneSetWrite = list(map( dateToStr, workDoneSet ))

	#encoded = Encoder().encode(workDoneSetWrite)
	encoded = json.dumps(workDoneSetWrite, cls=Encoder, indent=4)
	open(filename, 'w').write(encoded)

def fromFile(filename):
	"""
	Return: set of WorkDone ordered by chronological time.
	"""

	jl = json.loads( open(filename).read() )
	workUnits = []
	for item in jl:
		workDone = WorkDone( item['type'], item['length'], item['comment'], dateStrToDateTime(item['date']) )
		workUnits.append(workDone)
	workUnits.sort( key= lambda x: x.date )
	return workUnits

def createTestData():
	workUnits = []
	workUnits.append( WorkDone('test', 1, 'test item 1',datetime.datetime.fromtimestamp(1443888930.2002168, datetime.timezone.utc) ) )
	workUnits.append( WorkDone('test', 3.1, 'test\n\n\n item 2', datetime.datetime.fromtimestamp(1443888931.2002168, datetime.timezone.utc)))
	return workUnits

def unitTests():
	filename = os.path.join(options.utFolder, 'unit-tests-%s.json' % __file__)
	workUnits = createTestData()
	toFile(filename, workUnits)

	wdRead = fromFile(filename)
	for i in range(len(workUnits)):
		assert workUnits[i].type == wdRead[i].type
		assert workUnits[i].length == wdRead[i].length
		assert workUnits[i].comment == wdRead[i].comment
		assert workUnits[i].date == wdRead[i].date
	
	# Test default CTOR / serialization.
	workUnits.append( WorkDone('test', 1.1, 'test3') )
	toFile(filename, workUnits)
	wdRead = fromFile(filename)

if __name__ == '__main__':
	unitTests()



