"""
something like:

goal:::(name=test_goal,start=2024-11-07,end=2024-12-01,progress=0.0)
"""

import sys
import os
import shutil
import argparse
import datetime
import re
import math
import time
import json

import dcore.osrun as osrun 
import dcore.data as dcore_data
import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.meta as meta
import dcore.apps.dnotes.score as score
import dcore.apps.dnotes.search as search
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.options as options
import dcore.apps.dnotes.background.bg_lib as bg_lib

_meta_shell_command = 'bg_goal_track'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a',
                        '--aaa',
                        action='store_true',
                        help='...')
    return parser.parse_args()

def aaa():
    files = util.get_all_note_files()
    for ff in files:
        metas = meta.extract(ff, open(ff, 'r').read())
        for mm in metas:
            if mm.meta_type == 'goal':
                print(mm)

if __name__ == '__main__':
    G_ARGS = get_args()
    aaa()

