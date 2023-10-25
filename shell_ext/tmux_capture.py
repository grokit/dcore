
import os
import datetime

import dcore.data as data

_meta_shell_command = 'tmux_capture'

_SAFESET = set('0123456789-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
def safeset(ss):
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
    data.createDirIfNotExist(folder)

    pattern = 'tmux_capture'
    i = 0
    filename = find(folder, pattern, i)
    while os.path.exists(filename):
        i += 1
        filename = find(folder, pattern, i)

    cmd = f'tmux capture-pane -S -1000000 && tmux save-buffer {filename}'
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


