"""
# Bugs
- If you manually add other nodes, they will get deleted on read/write.
"""

import taskdone
import tasktime

import xml.etree.ElementTree as etree
import xml.dom.minidom
import os


def convertToPrettyPrint(element):
    strXml = etree.tostring(element)
    strPrettyXml = xml.dom.minidom.parseString(strXml).toprettyxml()
    return strPrettyXml


class TaskDoneList_ToHD:

    @staticmethod
    def write(lstTaskDone, strFilename):
        taskDoneXmlDB_Root = etree.Element('TaskDoneList')
        for taskDone in lstTaskDone:
            taskDone_Node = etree.Element('TaskDone')

            # All the attributes
            ele = etree.Element('Name')
            ele.text = taskDone.getName()
            taskDone_Node.append(ele)
            ele = etree.Element('CreationTime')
            ele.text = tasktime.transformTimeStruct_ToTaskStandardTime(
                taskDone.getCreationTime())
            taskDone_Node.append(ele)
            ele = etree.Element('TimeSpent')
            ele.text = str(taskDone.getTimeSpent())
            taskDone_Node.append(ele)
            ele = etree.Element('Comments')
            ele.text = taskDone.getComments()
            taskDone_Node.append(ele)

            taskDoneXmlDB_Root.append(taskDone_Node)

        # toXmlStr = etree.tostring(taskDoneXmlDB_Root)
        toXmlStr = convertToPrettyPrint(taskDoneXmlDB_Root)
        fh = open(strFilename, 'w')
        fh.write(toXmlStr)
        fh.close()


class TaskDoneList_FromHD:

    @staticmethod
    def __buildBlankTaskListFile(strFilename):
        taskDoneXmlDB_Root = etree.Element('TaskDoneList')
        toXmlStr = etree.tostring(taskDoneXmlDB_Root)
        fh = open(strFilename, 'w')
        fh.write(toXmlStr.decode('utf-8'))
        fh.close()

    @staticmethod
    def __extractTask(taskDoneXml):
        taskDone = None
        try:
            sName = (taskDoneXml.find('Name').text).strip()
            # print('Processing: %s' % sName)
            sCreationTime = (taskDoneXml.find('CreationTime').text).strip()
            fTimeSpent = float(taskDoneXml.find('TimeSpent').text)
            sComments_el = taskDoneXml.find('Comments').text
            if sComments_el is None:
                sComments_el = ''
            sComments = sComments_el.strip()
            taskDone = taskdone.TaskDone(sName,
                                         fTimeSpent,
                                         sComments,
                                         sCreationTime)
        except AttributeError as except_ae:
            print('Error: invalid input: %s' % taskDoneXml)
            print('(Original exception: %s)' % except_ae)
        return taskDone

    @staticmethod
    def read(strFilename):
        if not os.path.isfile(strFilename):
            TaskDoneList_FromHD.__buildBlankTaskListFile(strFilename)

        taskDoneXmlDB_Tree = etree.parse(strFilename)
        taskDoneXmlDB_Root = taskDoneXmlDB_Tree.getroot()

        lstTaskDone = []
        lstTaskDoneXml = taskDoneXmlDB_Root.findall('TaskDone')
        for taskDoneXml in lstTaskDoneXml:
            taskDone = TaskDoneList_FromHD.__extractTask(taskDoneXml)
            if taskDone is not None:
                lstTaskDone.append(taskDone)

        return lstTaskDone
