
_meta_shell_command = 'format_python'

import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    cmd = "autopep8 --in-place --aggressive --aggressive %s" % args.filename
    print(cmd)
    os.system(cmd)
