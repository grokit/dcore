
_meta_shell_command = 'cpprun'

import os
import argparse

def isCppFile(filename):
    if os.path.splitext(filename)[1] in ['.cpp', '.hpp', '.cc']:
        return True
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, nargs='?', default = None)
    args = parser.parse_args()

    filec = []
    if args.file != None:
        filesc = [args.file]
    else:
        files = os.listdir('.')
        filesc = [file for file in files if isCppFile(file)]

    rv = 0;
    for file in filesc:
        cmd = 'g++ -Wl,--no-as-needed -std=c++11 -pthread %s -o %s.bin' % (file, file)
        #cmd = 'clang -std=c++11 %s -o %s.bin' % (file, file)
        print(cmd)
        rv |= os.system(cmd)

    skipRun = True

    if not skipRun:
        if rv == 0:
            os.system('./' + filesc[0] + '.bin > ' + filesc[0] + '.out')
            os.system('cat ./' + filesc[0] + '.out')
    else:
        print('Run skipped, change script if want other behavior.')
