
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
    parser.add_argument('-r', '--run', action="store_true")
    args = parser.parse_args()

    filec = []
    if args.file != None:
        filesc = [args.file]
    else:
        files = os.listdir('.')
        filesc = [file for file in files if isCppFile(file)]

    rv = 0;
    for file in filesc:
        cmd = 'g++ -Wl,--no-as-needed -std=c++14 -pthread %s -o %s.bin' % (file, file)

        #using clang, experimental
        #cmd = 'clang -std=c++11 %s -o %s.bin' % (file, file)

        print(cmd)
        rv |= os.system(cmd)

    if args.run == True:
        if rv == 0:
            cmd = './' + filesc[0] + '.bin > ' + filesc[0] + '.out'
            print(cmd)
            os.system(cmd)
            cmd = 'cat ./' + filesc[0] + '.out'
            os.system(cmd)
    else:
        print('Run skipped, see command-line arguments if want to auto-run output.')
