
import os
import argparse

_meta_shell_command = 'linediff'

def getArgs():

    parser = argparse.ArgumentParser()

    parser.add_argument('left')
    parser.add_argument('right')
    
    parser.add_argument('-w', '--write', action = "store_true")
    
    args = parser.parse_args()
    
    return args
    
def fileToDict(filename):
    
    fh = open(filename, 'r')
    lines = fh.readlines()
    fh.close()
    
    D = {}
    for line in lines:
        line = line.strip()
        
        D[line] = True
    
    return D

if __name__ == '__main__':
    
    args = getArgs()
    print(args)
    
    A = fileToDict(args.left)
    B = fileToDict(args.right)

    InLeftButNotRight = []
    for k, v in A.items():
        if k not in B:
            InLeftButNotRight.append(k)
        
    InLeftButNotRight.sort()
    
    if args.write:
        fh = open(args.left + '.InLeftButNotRight', 'w')
        fh.write("\n".join(InLeftButNotRight))
        fh.close()
    else:
        print("\n".join(InLeftButNotRight))
    



