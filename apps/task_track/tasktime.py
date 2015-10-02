
import time


def getTaskStandardTime_Now():
    timeYMDHM = time.strftime("%Y-%m-%d %H:%M")
    return timeYMDHM


def getTaskStandardTime_NextMidnight():
    timeYMDHM = time.strftime("%Y-%m-%d 23:59")
    return timeYMDHM


def getTaskStandardTime_FirstThingThisMorning():
    timeYMDHM = time.strftime("%Y-%m-%d 00:00")
    return timeYMDHM


def getTimeStruct_FirstThingThisMorning():
    timeYMDHM = getTaskStandardTime_FirstThingThisMorning()
    return transformTaskStandardTime_ToTimeStruct(timeYMDHM)


def transformTaskStandardTime_ToTimeStruct(strTaskStandardTime):
    time9Tuple = time.strptime(strTaskStandardTime, "%Y-%m-%d %H:%M")
    return time9Tuple


def transformTimeStruct_ToTaskStandardTime(timeStruct):
    time9Tuple = time.strftime("%Y-%m-%d %H:%M", timeStruct)
    return time9Tuple


def test_module():
    strTaskStandardTime = getTaskStandardTime_Now()
    print(strTaskStandardTime)
    timeStruct = transformTaskStandardTime_ToTimeStruct(strTaskStandardTime)
    print(timeStruct)
    assert(getTimeStruct_FirstThingThisMorning() <= timeStruct)

if __name__ == '__main__':
    test_module()
