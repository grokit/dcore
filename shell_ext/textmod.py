
import argparse

_meta_shell_command = 'textmod'

def getArgs():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('tomod', nargs='+')
    parser.add_argument('-m', '--mode', default = 'upper', help='upper, lower, crazy, ascii')
    # maybe just have -a for ascii, etc
    
    args = parser.parse_args()
    
    return args

if __name__ == '__main__':
    
    args = getArgs()
    #print(args)
    
    txt = args.tomod
    
    if args.mode.lower() == 'upper':
        txt = " ".join(args.tomod).upper()
    
    if args.mode.lower() == 'lower':
        txt = " ".join(args.tomod).lower()
    
    if args.mode.lower() == 'ascii':
        asc = []
        for x in " ".join(args.tomod):
            asc.append( str(ord(x)) )
        txt = " ".join(asc)        
        
    if args.mode.lower() == 'crazy':
        
        T = []
        txt = " ".join(args.tomod)
        for i in range(0, len(txt)):
            T.append( txt[i].lower() if i % 2 == 0 else txt[i].upper() )
        txt = "".join(T)
        
    print(txt)