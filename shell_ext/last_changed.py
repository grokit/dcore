
_meta_shell_command = 'last_changed'

import os
import argparse
import glob


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--ext', help="Only allow this extension, e.g. png")
    args = parser.parse_args()

    filesAndChange = []

    globPattern = '**'
    if args.ext:
        globPattern = '**/*.%s' % args.ext
        print('Using glob pattern: %s.' % globPattern)
    for filename in glob.iglob('%s' % globPattern, recursive=True):
        filesAndChange.append((os.path.getmtime(filename), filename))

    filesAndChange.sort(reverse=True)
    filesAndChange = filesAndChange[0:20]
    for gmtime, filename in filesAndChange:
        print(filename)

