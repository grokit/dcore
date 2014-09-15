
import os
import argparse

_meta_shell_command = 'linesort'

def getArgs():

    parser = argparse.ArgumentParser()

    parser.add_argument('file')
    
    parser.add_argument('-w', '--write', action = "store_true")
    
    args = parser.parse_args()
    
    return args

if __name__ == '__main__':
    
    args = getArgs()
    
    fh = open(args.file, 'r')
    fc = fh.readlines()
    fh.close()

    fc.sort()
    
    if args.write:
        fh = open(args.file + '.linesorted', 'w')
        fh.write("".join(fc))
        fh.close()
    else:
        print("".join(fc))
        