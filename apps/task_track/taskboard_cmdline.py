
import taskstats
import tasktime

import time


class Exception_TaskBoard(Exception):
    pass


def render_tasklist(lstTaskDone, strTaskName):

    #
    # Only keep tasks that match the name
    #

    lstTaskDone = taskstats.filter_name(lstTaskDone, strTaskName)

    #
    # For every day during the last month, was the task done?
    #

    daysInAMonth = 30.4368499
    secondsInADay = 24 * 60 * 60
    timeInSecondsSinceEpochAtMidnight = time.mktime(
        tasktime.transformTaskStandardTime_ToTimeStruct(tasktime.getTaskStandardTime_NextMidnight()))
    taskDoneXDaysAgo = {}
    for x in range(0, int(daysInAMonth - 1.0)):
        timeStruct_hb = time.localtime(
            timeInSecondsSinceEpochAtMidnight -
            x *
            secondsInADay)
        timeStruct_lb = time.localtime(
            timeInSecondsSinceEpochAtMidnight - (
                x + 1) * secondsInADay)
        lstTaskDoneThatDay = taskstats.filter_betweenTime(
            lstTaskDone, timeStruct_lb, timeStruct_hb)
        isDoneThatDay = False
        if len(lstTaskDoneThatDay) >= 1:
            isDoneThatDay = True
        taskDoneXDaysAgo[x] = isDoneThatDay

    #
    # Produce 'nice graphics on the command line' :P
    #

    strOut = "Statistics for task '%s' during the last 30 days:\n    " % strTaskName
    # strOut += '(%s)\n' % taskDoneXDaysAgo
    score = 0
    for wasTaskDone in taskDoneXDaysAgo.values():
        if wasTaskDone:
            strOut += 'O'
            score += 1
        else:
            strOut += 'X'

    strOut += '\n'
    score = score / len(taskDoneXDaysAgo)
    strOut += 'Score: %.2f' % score

    return strOut
