
_meta_shell_command = 'format_cpp'

import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    cmd = "astyle --style=bsd %s" % args.filename
    print(cmd)
    os.system(cmd)
