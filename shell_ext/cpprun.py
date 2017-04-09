
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
    parser.add_argument('-d', '--debug', action="store_true")
    parser.add_argument('-g', '--gmon', action="store_true")
    args = parser.parse_args()

    filec = []
    if args.file != None:
        filesc = [args.file]
    else:
        files = os.listdir('.')
        filesc = [file for file in files if isCppFile(file)]

    rv = 0;
    for file in filesc:
        #cmd = 'g++ -Wl,--no-as-needed -std=c++14 -pthread %s -o %s.bin' % (file, file)

        #using clang, experimental
        #cmd = 'clang -std=c++11 %s -o %s.bin' % (file, file)
        cmd = 'clang++ -stdlib=libstdc++ -std=c++1z %s -o %s.tmpbin' % (file, file)
        if args.debug:
            print('Making debug build.')
            cmd += ' -g'
            # then use:
            # gdp -tui <bin>
            # https://sourceware.org/gdb/onlinedocs/gdb/Backtrace.html
        if args.gmon:
            # http://www.math.utah.edu/docs/info/gprof_3.html#SEC3
            print('Making profiling build. Look at gmon.out after.')
            cmd += ' -pg'

        print(cmd)
        rv |= os.system(cmd)

    args.run = True
    if args.run == True:
        if rv == 0:
            cmd = './' + filesc[0] + '.tmpbin > ' + filesc[0] + '.tmpout'
            print(cmd)
            os.system(cmd)
            cmd = 'cat ./' + filesc[0] + '.tmpout'
            os.system(cmd)
            if args.gmon:
                "gprof sol01-simple-recursion-TLE.cpp.tmpbin gmon.out > gmon.txt"
                cmd = 'gprof %s gmon.out > gmon.txt' % (filesc[0] + '.tmpbin')
                print(cmd)
                os.system(cmd)
    else:
        print('Run skipped, see command-line arguments if want to auto-run output.')
