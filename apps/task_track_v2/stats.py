"""
# TODO

- Hold off this. Just display raw data in graph + on-track / not on track first.
"""

import work_unit

def chunkWorkDoneByDays(workDoneArray):
	"""
	Split in an array where:
	0: list of WorkDone in the last 24 hours.
	1: ... the next 24 hours after that
	2: ... so on.
	"""
	assert type(workDoneArray) == list
	if len(workDoneArray) == 0:
		return
	assert type(workDoneArray[0]) == work_unit.WorkDone

	byDay = []
	raise NotImplemented()

	# Type checks...
	if len(byDay) > 0:
		assert type(byDay[0]) == list
		if len(byDay[0]) > 0:
			assert type(byDay[0][0]) == work_unit.WorkDone
	
	return byDay

