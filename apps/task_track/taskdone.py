
import time

import tasktime


class TaskDone:

    def __init__(
        self,
        sName,
        fTimeDecimalHours,
        sComments,
            sCreationTime=None):
        self.__sName = sName
        self.__fTime = fTimeDecimalHours
        self.__sComments = sComments
        if sCreationTime is None:
            self.__sCreationTime = tasktime.getTaskStandardTime_Now()
        else:
            self.__sCreationTime = sCreationTime

    def __str__(self):
        nStr = "Name: %s" % (self.__sName)
        nStr += " " * (15 - len(nStr))
        tStr = "time: %s" % (self.__fTime)
        tStr += " " * (13 - len(tStr))
        tiStr = "at: %s" % (self.__sCreationTime)
        tiStr += " " * (15 - len(tStr))

        cStr = "comment(s): %s" % (self.__sComments)

        return nStr + '\n  ' + tStr + '\n  ' + tiStr + '\n  ' + cStr + '\n'

    def getName(self):
        return self.__sName

    def getTimeSpent(self):
        return self.__fTime

    def getCreationTime(self):
        return tasktime.transformTaskStandardTime_ToTimeStruct(self.__sCreationTime)

    def getComments(self):
        return self.__sComments
