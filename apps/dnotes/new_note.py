"""
# Overview 

Create a note document (or append to if already exists) in the note_db folder and inserts metadata.

## Important Characteristics

- Scatter and merge: be able to take one-off notes of little importance, but late when a lot of small things are scattered at different places, make it obvious (thourgh search-and-match) and easy to merge.

- Main design characteristic: if you have an idea, as short a time possible to be writing.
    -> put the friction at ingest time if necessary.

## Insert file as journal entry (directly in text file)
    
    $ nn < file

## Save a copy of file in same directory as journal
    
    $ nn -f filename

# TODOs

## As
## Bs
- nn replace the time meta
## Cs


"""

_meta_shell_command = 'nn'

import os
import datetime
import argparse
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


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t',
                        '--force_time_tagging',
                        action='store_true',
                        default=False)
    return parser.parse_args()


def annotateDateIfNotAlreadyDone(file, force=False):
    with open(file, 'r') as fh:
        fileContent = fh.read()

    if force or 'time%s' % options.MSEP not in fileContent:
        annotation = 'time%s' % options.MSEP + dateForAnnotation() + '\n'

        with open(file, 'w') as fh:
            fh.write(annotation + '\n' + fileContent)


if __name__ == '__main__':
    args = get_args()

    fullpath = data.get_ingest_fullpath()
    util.createFolderIfNotExist(os.path.split(fullpath)[0])
    util.createFileIfNotExist(fullpath)

    annotateDateIfNotAlreadyDone(fullpath, args.force_time_tagging)
    util.openInEditor(fullpath)
