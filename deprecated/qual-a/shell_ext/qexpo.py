
_meta_shell_command = 'qexpo'

import sys
import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()

    parser.add_argument('numbers', nargs='+')
    parser.add_argument('-f', '--file', type=str)
    
    args = parser.parse_args()
    
    lst = args.numbers
    
    assert len(lst) == 2
    
    a = int(lst[0])
    b = int(lst[1])
    
    r = a**b
    
    if args.file is not None:
        fh = open(args.file, 'wb')
        fh.write(str(r).encode('ASCII'))
        fh.close()
    
    print(r)
    