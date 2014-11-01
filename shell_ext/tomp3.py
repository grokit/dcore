_meta_shell_command = 'tomp3'

import os
import re
import argparse
import shutil
import time

mp3_dir = '/media/david/SANSA CLIPP/MUSIC'
mp3_in_folders = [os.path.expanduser(f) for f in ['~/Desktop/podcasts', '~/Downloads']]

def getArgs():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-m', '--move_old_files', default=True)
    
    args = parser.parse_args()
    return args

def isMusic(filename):
    return re.search(r'.*mp.$', filename.lower())

if __name__ == '__main__':
    args = getArgs()
    print(args)

    print('Mp3 player path: %s.\n' % mp3_dir)

    if not os.path.isdir(mp3_dir):
        raise Exception('Mp3 player not plugged in.')

    print('Files already on mp3:')
    for file in os.listdir(mp3_dir):
        print(" "*4 + file)

    if args.move_old_files == True:
        nowF = time.strftime("%Y-%m-%d", time.localtime())

        pathOld = os.path.join(mp3_dir, nowF)
        if not os.path.isdir(pathOld):
            os.mkdir(pathOld)

        for file in [os.path.join(mp3_dir, f) for f in os.listdir(mp3_dir) if isMusic(f)]:
            head = os.path.split(file)[1]
            to = os.path.join(pathOld, head)
            print('Moving %s to %s.' % (file, to))
            shutil.move(file, to) 

    filesMove = []
    for mp3_in in mp3_in_folders:
        filesMove += [os.path.join(mp3_in, f) for f in os.listdir(mp3_in) if isMusic(f) is not None]

    print('\nFiles to transfer to mp3:')
    for file in filesMove:
        print(" "*4 + os.path.abspath(file))
    print('')

    for file in filesMove:
        head = os.path.split(file)[1]
        to = os.path.join(mp3_dir, head)
        print('Moving %s to %s.' % (file, to))
        shutil.move(file, to) 
