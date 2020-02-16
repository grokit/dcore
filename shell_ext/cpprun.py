_meta_shell_command = 'cpprun'

import os
import argparse


def isCppFile(filename):
    if os.path.splitext(filename)[1] in ['.cpp', '.hpp', '.cc']:
        return True
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, nargs='?', default=None)
    parser.add_argument('-r', '--run', default=True, action="store_true")
    parser.add_argument('-d', '--debug', action="store_true")
    parser.add_argument('-g', '--gmon', action="store_true")
    parser.add_argument('-v', '--valgrind', action="store_true")
    parser.add_argument('-p', '--profile', action="store_true")
    args = parser.parse_args()

    for i in range(200):
        print('')
    print('-~' * 30 + '===')

    filec = []
    if args.file != None:
        filesc = [args.file]
    else:
        files = os.listdir('.')
        filesc = [file for file in files if isCppFile(file)]

    assert len(filesc) == 1
    rv = -1
    file = os.path.abspath(filesc[0])
    #cmd = 'g++ -Wl,--no-as-needed -std=c++14 -pthread %s -o %s.tmpbin' % (file, file)
    # no -fcoroutines-ts in g++ so far
    cmd = 'g++ -Wl,--no-as-needed -std=c++2a -pthread %s -o %s.tmpbin' % (file, file)

    # Extra warnings
    if False:
        cmd = 'g++ -Wall -Wextra -std=c++14 -pthread %s -o %s.tmpbin' % (file,
                                                                         file)

    #using clang, experimental
    #cmd = 'clang -std=c++11 %s -o %s.bin' % (file, file)
    #cmd = 'clang++-4.0 -stdlib=libstdc++ -std=c++1z %s -o %s.tmpbin' % (file, file)
    #cmd = 'clang++-4.0 -stdlib=libc++ -std=c++1z %s -o %s.tmpbin' % (file, file)
    if args.debug:
        print('Making debug build.')
        cmd += ' -g'
        # needed for clang to properly display some variables
        # see: https://stackoverflow.com/questions/41745527/cannot-view-stdstring-when-compiled-with-clang
        cmd += ' -D_GLIBCXX_DEBUG'
        # then use:
        # gdp -tui <bin>
        # https://sourceware.org/gdb/onlinedocs/gdb/Backtrace.html
    if args.gmon:
        # http://www.math.utah.edu/docs/info/gprof_3.html#SEC3
        print('Making profiling build. Look at gmon.out after.')
        cmd += ' -pg'

    print(cmd)
    rv = os.system(cmd)

    if args.run == True:
        assert rv == 0
        cmd = file + '.tmpbin | tee ' + file + '.tmpout'
        print(cmd)

        if args.valgrind:
            cmd = 'valgrind ' + cmd

        if args.profile:
            # use kcachegrind to view file
            cmd = 'valgrind --tool=callgrind ' + cmd + ';kcachegrind `ls callgrind.out.* -t | tail -n 1`'

        os.system(cmd)

        if args.gmon:
            "gprof sol01-simple-recursion-TLE.cpp.tmpbin gmon.out > gmon.txt"
            cmd = 'gprof %s gmon.out > gmon.txt' % (file + '.tmpbin')
            print(cmd)
            os.system(cmd)
        if args.debug:
            cmd = 'gdb -tui %s' % (file + '.tmpbin')
            print(cmd)
            os.system(cmd)

    else:
        print(
            'Run skipped, see command-line arguments if want to auto-run output.'
        )
