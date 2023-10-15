
import os

import dcore.data as data

_meta_shell_command = 'tmux_capture'

def find(pattern, i):
    return os.path.expanduser(f'~/{pattern}_{i:04d}.log')

if __name__ == '__main__':
    pattern = 'tmux_capture'
    i = 0
    filename = find(pattern, i)
    while os.path.exists(filename):
        i += 1
        filename = find(pattern, i)

    cmd = f'tmux capture-pane -S -100000 && tmux save-buffer {filename}'
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


