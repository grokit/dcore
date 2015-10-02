"""
# TODO

## As

- Export to html or image for goal
- Be able to have weekly overview
- Be able to set goals

## Bs

"""

DEFAULT_TASKDONELIST_DB_FILE = 'TaskDoneList_DB.xml'

import serialization_xml as serializer
import taskstats
import taskboard_cmdline
import taskdone

import optparse

import os
import time
import sys


def python27or31_input(strQ):
	try:
		if sys.version_info.major < 3:
			input_ent = raw_input(strQ)
		else:
			input_ent = input(strQ)
	except AttributeError:
		print("Warning: cannot find python version, trying intput()")
		input_ent = input(strQ)
	return input_ent


def processCmdLineOptions():

	parser = optparse.OptionParser(usage="%prog [option(s)]")

	parser.add_option("--usedb",
					  action="store", type='string', dest="custom_db", default=None,
					  help="Specify the database filename.")

	(options, positional_args) = parser.parse_args()

	dictOptions = {}
	if options.custom_db is not None:
		dictOptions['DBFileToUse'] = options.custom_db
	else:
		dictOptions['DBFileToUse'] = DEFAULT_TASKDONELIST_DB_FILE

	# print("Command line options: %s" % dictOptions)
	return dictOptions


def __inputNameNTime():
	name = python27or31_input("Name?\n")
	time = ''
	while not isinstance(time, type(3.1337)):
		try:
			time = float(python27or31_input("Time (decimal hours)?\n"))
		except ValueError:
			print("Invalid value... try again")
	return (name, time)


def enterTask(name=None, time=None, comments=None):

	dbFilename = getDBFilename()
	lstTaskDone = serializer.TaskDoneList_FromHD.\
		read(dbFilename)

	if name is None:
		assert time is None
		(name, time) = __inputNameNTime()
	if comments is None:
		comments = python27or31_input("Comment(s)?\n")

	taskDone = taskdone.TaskDone(name, time, comments)
	lstTaskDone.append(taskDone)

	serializer.TaskDoneList_ToHD.write(lstTaskDone, dbFilename)


def listTasks():

	dbFilename = getDBFilename()
	print('Using DB file: %s.' % dbFilename)
	lstTaskDone = serializer.TaskDoneList_FromHD.read(dbFilename)

	print("Top times: ")
	dictTypeToTotalTime = taskstats.getDictOfType_TotalTime(lstTaskDone)
	# print only biggest 5
	dictTypeToTotalTime = sorted(dictTypeToTotalTime.items(),
								 key=lambda t: t[1], reverse=True)
	x = 0
	for item, key in dictTypeToTotalTime:
		top = "  {0}:{1}".format(item, key)
		while len(top) < 20:
			top = top.replace(':', ': ')
		print(top)
		x = x + 1
		if x >= 5:
			break
	print("Global grand total: %s" % taskstats.getTotalTime(lstTaskDone))

	print("\nDone today: ")
	for taskDoneToday in taskstats.getDoneToday(lstTaskDone):
		print(taskDoneToday)

	print("Total times today: ")
	dictTypeToTotalTime = taskstats.getDictOfType_TotalTime(
		taskstats.getDoneToday(lstTaskDone))
	print("  " + str(dictTypeToTotalTime))
	print("Today grand total:  %s" % taskstats.getTotalTime(
		  taskstats.getDoneToday(lstTaskDone)))
	print("-" * 80)


def getDBFilename():
	dictOptions = processCmdLineOptions()
	dbFilename = dictOptions['DBFileToUse']
	#folder = os.path.dirname(os.path.realpath(__file__))
	folder = os.path.expanduser('~/sync')
	dbFilename = folder + '/' + dbFilename
	return dbFilename

def listStatTaskBoard(strTaskName):
	print('listStatTaskBoard: %s' % strTaskName)

	lstTaskDone = serializer.TaskDoneList_FromHD.read(getDBFilename())

	strTaskBoard = taskboard_cmdline.render_tasklist(lstTaskDone, strTaskName)
	print(strTaskBoard)
