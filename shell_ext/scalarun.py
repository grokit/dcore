
_meta_shell_command = 'srun'

import os
import argparse

def isSourceFile(filename):
    if os.path.splitext(filename)[1] in ['.scala', '.sc']:
        return True
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_and_feed', type=str, nargs='?', default = None)
    args = parser.parse_args()

    filesc = [file for file in os.listdir('.') if isSourceFile(file)]
    assert len(filesc) == 1
    filesc = filesc[0]

    feed = None
    if args.file_and_feed is not None:
        feed = args.file_and_feed
    print('feed', feed)

    rv = 0
    os.system('mkdir out')
    cmd = 'scalac %s -d out' % (filesc)
    print(cmd)
    rv |= os.system(cmd)

    if rv == 0:
        classFile = [os.path.splitext(x)[0] for x in os.listdir('./out') if os.path.splitext(x)[1] == '.class' and x.find('$') == -1]

        if len(classFile) != 1:
            print("Don't know what to run from: %s." % classFile)
            exit(-1)
        classFile = classFile[0]

        feedStr = ''
        if feed is not None:
            feedStr = ' < %s ' % feed
        cmd = 'scala -cp ./out/ ' + classFile + feedStr + ' > ./out/' +classFile  + '.out'
        print(cmd)
        os.system(cmd)
        os.system('cat ./out/' + classFile + '.out')

