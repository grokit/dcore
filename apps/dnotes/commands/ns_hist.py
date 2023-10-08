"""
History of modified files: most recent, most often modified, etc.
"""

import sys
import os
import argparse
import re
import math
import time

import dcore.osrun as osrun 
import dcore.data as dcore_data
import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.meta as meta
import dcore.apps.dnotes.score as score
import dcore.apps.dnotes.search as search
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.options as options

_meta_shell_command = 'ns_hist'


def get_args():
    parser = argparse.ArgumentParser()
    # TODO: add option to remove files that don't exist anymore.
    parser.add_argument('-n', '--num_files',
                        type=int,
                        default=30, help='This is approximate.')
    parser.add_argument('-f',
                        '--root_folder',
                        nargs='?',
                        type=str,
                        default='')
    parser.add_argument('-s',
                        '--stats',
                        action='store_true',
                        help='If true, give the most often modified.')
    return parser.parse_args()

def process_git_log_output(stdout, root_folder):
    """
    In: output from git command.
    Out: array with raw output but small details such as normalized lines.
    """

    #path_ext = dcore_data.pathExt()

    out = []
    for line in stdout.splitlines():
        line = line.strip()
        if len(line) == 0: continue
        line = os.path.join(root_folder, line)
        line = os.path.abspath(line)
        # print(path_ext, line)
        #if path_ext in line: continue
        out.append(line)
    return out

def do_not_repeat(filelist):
    seen = set()
    out = []
    for ff in filelist:
        if ff in seen: continue
        seen.add(ff)
        out.append(ff)
    return out

def compute_repetition(filelist):
    mem = {}
    for ff in filelist:
        if ff not in mem:
            mem[ff] = 0
        mem[ff] += 1

    out = []
    for ff, rep in mem.items():
        out.append((rep, ff))
    out.sort(key=lambda x: x[0], reverse=True)
    return out


if __name__ == '__main__':
    G_ARGS = get_args()

    if G_ARGS.root_folder == '':
        root_folder = data.get_notes_root_folder()
        os.chdir(root_folder)
    else:
        root_folder = '.'

    if False:
        print(f'Using root_folder: {root_folder}.')

    overshoot = 100
    if G_ARGS.stats:
        overshoot = 1000
    # Note: -n {G_ARGS.num_files} is actually the number of previous commits looked at.
    rv, stdout, stderr = osrun.executeCmd(f"git log -n {G_ARGS.num_files + overshoot} --name-only --relative --pretty=format:'' .")
    assert rv == 0
    assert len(stderr) == 0

    filelist = process_git_log_output(stdout, root_folder)

    if G_ARGS.stats:
        file_and_rep = compute_repetition(filelist)
        file_and_rep = file_and_rep[0:G_ARGS.num_files]
        for rep, ff in file_and_rep:
            print(f'{rep:3d}: {ff}')
    else:
        filelist = do_not_repeat(filelist)
        if len(filelist) > G_ARGS.num_files:
            filelist = filelist[0:G_ARGS.num_files]
        for ff in filelist:
            print(ff)


