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
import work_unit
import date_convention


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
        ww.date = date_convention.dateTimeToStr(ww.date)
        return ww

    workDoneSetWrite = list(map(dateToStr, workDoneSet))

    #encoded = Encoder().encode(workDoneSetWrite)
    encoded = json.dumps(workDoneSetWrite,
                         cls=Encoder,
                         indent=4,
                         sort_keys=True)
    open(filename, 'w').write(encoded)


def fromFile(filename):
    """
	Return: set of WorkDone ordered by chronological time.
	"""

    jl = json.loads(open(filename).read())
    workUnits = []
    for item in jl:
        workDone = work_unit.WorkDone(
            item['type'], item['length'], item['comment'],
            date_convention.dateStrToDateTime(item['date']))
        # Fixed messed-up time file, only do to change timezone / apply offset.
        #workDone.date = workDone.date.replace(tzinfo=date_convention.timeZone)
        #workDone.date -= datetime.timedelta(hours=7)
        workUnits.append(workDone)
    workUnits.sort(key=lambda x: x.date)
    return workUnits


def createTestData():
    workUnits = []
    workUnits.append(
        work_unit.WorkDone(
            'test', 1, 'test item 1',
            datetime.datetime.fromtimestamp(1443888930.2,
                                            date_convention.timeZone)))
    workUnits.append(
        work_unit.WorkDone(
            'test', 3.1, 'test\n\n\n item 2',
            datetime.datetime.fromtimestamp(1443888931.2,
                                            date_convention.timeZone)))
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
        #print(workUnits[i].date)
        #print(wdRead[i].date)
        assert workUnits[i].date == wdRead[i].date

    # Test default CTOR / serialization.
    workUnits.append(work_unit.WorkDone('test', 1.1, 'test3'))
    toFile(filename, workUnits)
    wdRead = fromFile(filename)


if __name__ == '__main__':
    unitTests()
