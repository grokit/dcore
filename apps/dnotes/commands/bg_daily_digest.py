"""
Experimental: daily digest.
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
import dcore.apps.dnotes.bg_tasks as bg_tasks

_meta_shell_command = 'bg_daily_digest'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a',
                        '--aaa',
                        action='store_true',
                        help='...')
    return parser.parse_args()


if __name__ == '__main__':
    G_ARGS = get_args()
    bg_tasks.daily_digest()

