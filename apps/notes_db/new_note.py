"""
# Overview 

Create a note document (or append to if already exists) in the note_db folder and inserts metadata.

## Insert file as journal entry (directly in text file)
    
    $ nn < file

## Save a copy of file in same directory as journal
    
    $ nn -f filename

# TODO

- More search points if:
    - Search is in title
    - Has UUID
    - Has tag
    - Had an `important` or `todo` tag.

- critical.sh -> proper python script -- maybe produce html page.

- nn --sshot or something like that: copy last screenshot or last 1 hour screenshot to dir with last touched note.md file.
"""

_meta_shell_command = 'nn'

import os
import datetime
import argparse
import platform
import shutil

import data
import util

def dateForFile():
    return datetime.datetime.now().strftime("%Y-%m-%d")
    
def dateForFolder():
    return datetime.datetime.now().strftime("%Y-%m-%d")    
    
def dateForAnnotation():
    #:::bug: use same for all scripts, date.py or globals.py
    return datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
    
def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--force_time_tagging', action='store_true', default=False)
    return parser.parse_args()

def annotateDateIfNotAlreadyDoneg(file, force = False):
    with open(file, 'r') as fh:
        fileContent = fh.read()

    if force or 'time::' not in fileContent:
        annotation = 'time::' + dateForAnnotation() + '\n'

        with open(file, 'w') as fh:
            fh.write(annotation + '\n' + fileContent)

def openInEditor(noteFilename):
    if platform.system() == 'Windows':
        c = 'notepad %s' % noteFilename
    else:
        c = 'vim %s' % noteFilename
    os.system(c)

def resolveDataLocation(dataLocation = None):
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
