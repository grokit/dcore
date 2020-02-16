"""
# Overview 

Create a note document (or append to if already exists) in the note_db folder and inserts metadata.

## Important Characteristics

- Scatter and merge: be able to take one-off notes of little importance, but late when a lot of small things are scattered at different places, make it obvious (thourgh search-and-match) and easy to merge.

## Insert file as journal entry (directly in text file)
    
    $ nn < file

## Save a copy of file in same directory as journal
    
    $ nn -f filename

"""

_meta_shell_command = 'nn'

import os
import datetime
import argparse
import platform
import shutil

import data
import util

import options


def dateForFile():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def dateForFolder():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def dateForAnnotation():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t',
                        '--force_time_tagging',
                        action='store_true',
                        default=False)
    return parser.parse_args()


def annotateDateIfNotAlreadyDoneg(file, force=False):
    with open(file, 'r') as fh:
        fileContent = fh.read()

    if force or 'time%s' % options.MSEP not in fileContent:
        annotation = 'time%s' % options.MSEP + dateForAnnotation() + '\n'

        with open(file, 'w') as fh:
            fh.write(annotation + '\n' + fileContent)


def openInEditor(noteFilename):
    if platform.system() == 'Windows':
        c = 'notepad %s' % noteFilename
    else:
        c = 'vim %s' % noteFilename
    os.system(c)


def resolveDataLocation(dataLocation=None):
    if dataLocation == None:
        dataLocation = data.notesRoot()

    file = data.ingestFilename(dataLocation)
    return dataLocation, file


if __name__ == '__main__':
    args = getArgs()

    dataLocation, noteFilename = resolveDataLocation()
    util.createFolderIfNotExist(dataLocation)
    util.createFileIfNotExist(noteFilename)

    annotateDateIfNotAlreadyDoneg(noteFilename, args.force_time_tagging)
    openInEditor(noteFilename)
