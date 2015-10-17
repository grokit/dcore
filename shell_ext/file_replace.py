
import os
import argparse

_meta_shell_command = 'file_replace'

def getArgs():

    parser = argparse.ArgumentParser()

    parser.add_argument('-w', '--write_back', action = "store_true")
    
    parser.add_argument('-f', '--file', type = str, default = None, help="Files.")
    
    parser.add_argument('-o', '--replace_from', type = str, default = None, help="Thing to replace.")
    parser.add_argument('-t', '--replace_to', type = str, default = None, help="Replace with this.")
    
    # @@TODO: -s select files (default: all .cs)
    
    args = parser.parse_args()
    
    return args
    
if __name__ == '__main__':
    
    args = getArgs()
    print(args)
    
    if args.replace_from is None or args.replace_to is None:
        raise Exception("Invalid Arguments: %s." % args)
    
    files = [args.file]
    #files = os.listdir('.')
    #files = [file for file in files if file[-3:] == ".cs"]

    print(files)

    for file in files:
        
        print('Processing file: %s.' % file)
        
        fh = open(file, 'r')
        fc = fh.read()
        fh.close()
        
        replace_to = args.replace_to
        
        if replace_to == "%filename%":
            replace_to = file
        
        fc = fc.replace(args.replace_from, replace_to)
        
        suffix = '.repl'
        if args.write_back is True:
            suffix = ''
        fh = open(file + suffix, 'w')
        fh.write(fc)
        fh.close()
    
