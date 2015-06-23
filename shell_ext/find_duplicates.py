
import os
import argparse

_meta_shell_command = 'find_duplicates'

def getArgs():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args

def getAllFiles(rootdir = '.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append( os.path.join(dirpath, f) )
    return F

if __name__ == '__main__':
    
    args = getArgs()

    F = getAllFiles()
    H = {}
    for f in F:
        fp = f
        f = os.path.split(f)[1]
        if f not in H:
            H[f] = []
        H[f].append(fp)
    
    for k, v in H.items():
        if len(v) > 1:
            print(v)
