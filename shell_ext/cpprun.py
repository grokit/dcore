
_meta_shell_command = 'cpprun'

import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-f', '--file', type=str, default = None)
    args = parser.parse_args()
    
    filec = []
    if args.file != None:
        filesc = [args.file]
    else:
        files = os.listdir('.')
        filesc = [file for file in files if file[-3:].lower() == 'cpp']

    rv = 0;
    for file in filesc:
        cmd = 'g++ -std=c++11 %s -o %s.bin' % (file, file)
        #cmd = 'clang -std=c++11 %s -o %s.bin' % (file, file)
        print(cmd)
        rv |= os.system(cmd)

    if rv == 0:
        os.system('./' + filesc[0] + '.bin > ' + filesc[0] + '.out')
        os.system('cat ./' + filesc[0] + '.out')

