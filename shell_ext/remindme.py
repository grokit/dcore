
import argparse
import time

import dcore.private_data as private_data
import dcore.shell_ext.gmail as gmail

_meta_shell_command = 'reminder'

def getArgs():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('subject', nargs='+')
    parser.add_argument('-t', '--to', default= private_data.primary_email)
    parser.add_argument('-b', '--body', default='')
    
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    
    args = getArgs()
    print(args)
    
    gmail.do(args.to, " ".join(args.subject), args.body)
