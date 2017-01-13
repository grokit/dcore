
_meta_shell_command = 'hgpp'

import os

if __name__ == '__main__':

    cmds = []
    cmds.append('hg addremove -s75')
    cmds.append("hg commit -m 'hgpp'")

    for c in cmds:
        print(c)
        os.system(c)
