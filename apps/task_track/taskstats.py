
import tasktime

import time


class TaskStatsException(Exception):
    pass


def filter_name(lstTask, taskName):
    lstTaskNamedName = [task for task in lstTask if task.getName() == taskName]
    return lstTaskNamedName


def filter_afterTime(lstTask, timeStruct):

    lstTaskFiltered = []
    for task in lstTask:
        taskTimeStruct = task.getCreationTime()
        timeThisMorningStruct = tasktime.transformTaskStandardTime_ToTimeStruct(
            timeStruct)
        if taskTimeStruct > timeThisMorningStruct:
            lstTaskFiltered.append(task)
    return lstTaskFiltered


def filter_betweenTime(lstTask, timeStruct_lowerBound, timeStruct_upperBound):

    lstTaskFiltered = []
    for task in lstTask:
        taskTimeStruct = task.getCreationTime()
        if (taskTimeStruct > timeStruct_lowerBound) and (taskTimeStruct < timeStruct_upperBound):
            lstTaskFiltered.append(task)
    return lstTaskFiltered


def getDictOfType_TotalTime(lstTaskDone):

    taskMapByType = {}  # Dict: {TaskDoneName: listOfAllTaskDoneWithThisName}
    for taskDone in lstTaskDone:
        if taskMapByType.get(taskDone.getName()) is None:
            taskMapByType[taskDone.getName()] = [taskDone]
        else:
            taskMapByType[taskDone.getName()].append(taskDone)

    taskMapTimeByType = {}  # Dict: {TaskDoneName: totalTimeForAllThisTaskType}
    for taskDoneName in taskMapByType.keys():
        taskMapTimeByType[taskDoneName] = 0.0
        for taskDone in taskMapByType[taskDoneName]:
            taskMapTimeByType[taskDoneName] += taskDone.getTimeSpent()

    return taskMapTimeByType


def getTotalTime(lstTaskDone):
    totaltime = 0.0
    for taskDone in lstTaskDone:
        totaltime += taskDone.getTimeSpent()
    return totaltime


def getDoneToday(lstTask):
    lstTaskToday = \
        filter_afterTime(
            lstTask,
            tasktime.getTaskStandardTime_FirstThingThisMorning())
    return lstTaskToday
