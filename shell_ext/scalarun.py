
_meta_shell_command = 'srun'

import os
import argparse

def isSourceFile(filename):
    if os.path.splitext(filename)[1] in ['.scala', '.sc']:
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
        filesc = [file for file in files if isSourceFile(file)]

    rv = 0;
    for file in filesc:
        os.system('mkdir out')
        cmd = 'scalac %s -d out' % (file)
        print(cmd)
        rv |= os.system(cmd)

    if rv == 0:
        classFile = [os.path.splitext(x)[0] for x in os.listdir('./out') if os.path.splitext(x)[1] == '.class'][0]
        cmd = 'scala -cp ./out/ ' + classFile + ' > ./out/' +classFile  + '.out'
        print(cmd)
        os.system(cmd)
        os.system('cat ./out/' + classFile + '.out')
