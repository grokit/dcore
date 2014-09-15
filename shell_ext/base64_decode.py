
import base64
import argparse

_meta_shell_command = 'b64d -s'

def base64decode(str):
    return base64.b64decode(str) # this returns bytes!!
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--string_decode_or_encode', nargs='+')
    parser.add_argument('-f', '--filename')

    args = parser.parse_args()
    
    if args.filename is not None:
        fh = open(args.filename, 'r')
        b64c = fh.read()
        fh.close()
        
        print( base64decode( b64c.encode() ) )
        exit(0)        
    
    string_decode_or_encode = ""
    if type(args.string_decode_or_encode) == type([]):
        string_decode_or_encode = " ".join(args.string_decode_or_encode)    
    
    print( base64decode( string_decode_or_encode ) )

    