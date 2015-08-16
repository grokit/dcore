
_meta_shell_command = 'gitpp'

import os


if __name__ == '__main__':

    cmds = []
    cmds.append('git add --all :/')
    cmds.append('git commit -a -m "gitpp: auto commit"')

    for c in cmds:
        print(c)
        os.system(c)
