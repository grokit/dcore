"""
"""

import os
import argparse

import dcore.utils as dutils

import dcore.apps.dnotes.search as search
import dcore.apps.dnotes.meta as meta
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.score as score
import dcore.apps.dnotes.options as options

_meta_shell_command = 'import_todos'

import sys

def get_args():
    parser = argparse.ArgumentParser()
    return parser.parse_args()

def funky_sort(line):
    line = line.lower()
    if options.MSEP not in line:
        return 'z'*10
    return line[line.index(options.MSEP):]

def funky_filter(line):
    line = line.lower()
    if f'{options.MSEP}a' in line:
        return True
    if f'{options.MSEP}b' in line:
        return True
    if f'{options.MSEP}c' in line:
        return True
    return False

if __name__ == '__main__':
    args = get_args()

    filenames = util.get_all_note_files()

    to_insert_list = []
    matches = search.extractMatchSetsFromFiles(filenames, f'todo{options.MSEP}')

    filename = util.select_filename_by_uuid('todo_r554')
    todo_content = open(filename, 'r').read()

    # note: will not put annotations in todo inside todo
    matches = [mm for mm in matches if funky_filter(mm.line) and mm.line.strip() not in todo_content]
    matches = sorted(matches, key=lambda x: funky_sort(x.line), reverse=False)

    sep= '\n\t'
    for mm in matches:
        to_insert_list.append(f'{mm.filename}{sep}{mm.line.strip()}')

    cut_marker_begin = 'INSERT-TODO-A-BEGIN'
    cut_marker_end = 'INSERT-TODO-A-END'

    to_insert_list = [tt + '\n' for tt in to_insert_list]
    content = dutils.insert_cut(filename, cut_marker_begin, cut_marker_end, to_insert_list)
    with open(filename, 'w') as fh:
        fh.write(content)

