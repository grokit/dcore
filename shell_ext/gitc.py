_meta_shell_command = 'gitc'

import os
import sys

if __name__ == '__main__':

    assert len(sys.argv) > 1

    comment = " ".join(sys.argv[1:])

    cmds = []
    cmds.append('git add --all :/')
    cmds.append('git commit -a -m "%s"' % comment)

    for c in cmds:
        print(c)
        os.system(c)
