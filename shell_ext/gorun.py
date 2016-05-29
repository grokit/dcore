
_meta_shell_command = 'gorun'

import os
import subprocess
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--run', action="store_true", default=True)
    args = parser.parse_args()

    cmd = 'go build -o bin'
    print(cmd)
    r = os.system(cmd)
    r = r & 0xffff

    if r == 0 and args.run == True:
        cmd = './bin > std.out'
        print(cmd)
        os.system(cmd)
        cmd = 'cat ./std.out'
        os.system(cmd)
    else:
        print('Run skipped, see command-line arguments if want to auto-run output.')
