"""
tmux_capture: capture tmux content to a file.

# TODO
"""
import os
import datetime
import argparse

import dcore.data as data
import dcore.utils as utils

_meta_shell_command = 'tmux_capture'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--open', action='store_true', help='Open the file in a text editor after capture.')
    parser.add_argument('-c', '--cat', action='store_true', help='Print the file after capture.')
    args = parser.parse_args()
    return args

_SAFESET = set('0123456789-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
def safeset(ss):
    # TODO: replace with data.date_safe_for_filename()
    out = []
    for cc in ss:
        if cc in _SAFESET:
            out.append(cc)
        else:
            out.append('_')
    return "".join(out)

def date_now_iso_8601_safe_folder():
    return safeset(datetime.datetime.now().astimezone().isoformat())

def find(folder, pattern, i):
    return os.path.expanduser(os.path.join(folder, f'{pattern}_{date_now_iso_8601_safe_folder()}.log'))

if __name__ == '__main__':
    folder = os.path.join(data.logsdir(), 'tmux')
    G_ARGS = get_args()
    data.createDirIfNotExist(folder)

    if G_ARGS.open:
        files = os.listdir(folder)
        filename = os.path.join(folder, max(files, key=lambda ff: os.path.getmtime(os.path.join(folder, ff))))
        utils.openInEditor(filename)

    pattern = 'tmux_capture'
    i = 0
    filename = find(folder, pattern, i)
    while os.path.exists(filename):
        i += 1
        filename = find(folder, pattern, i)

    cmd = f'tmux capture-pane -J -S- -E- && tmux save-buffer {filename}'
    print(cmd)
    os.system(cmd)

    with open(filename, 'r') as fh:
        out = []
        found_delim = False
        for line in fh.readlines():
            if data.cls_file_delimiter() in line:
                out = []
                found_delim = True
            out.append(line)

    if found_delim:
        with open(filename, 'w') as fh:
            fh.write("".join(out))

    if G_ARGS.cat:
        with open(filename, 'r') as fh:
            for line in fh.readlines():
                print(line, end='')



