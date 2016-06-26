
_meta_shell_command = 'javarun'

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
        filesc = [file for file in files if os.path.splitext(file)[1] == '.java']

    rv = 0;
    for file in filesc:
        cmd = 'javac %s' % file
        print(cmd)
        rv |= os.system(cmd)

    if rv == 0:
        os.system('echo begin > out.out')
        for file in [f.replace('.class', '') for f in os.listdir('.') if '.class' in f]:
            cmd = 'java %s >> out.out' % file
            print(cmd)
            os.system(cmd)
            os.system('cat out.out')

