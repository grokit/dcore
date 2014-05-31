
import base64
import argparse

_meta_shell_command = 'b64e'

def base64encode(str):
    
    if type(str) == type(""):
        bytes = str.encode()
    else:
        bytes = str
    return base64.b64encode(bytes)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--string_decode_or_encode', nargs='+')
    parser.add_argument('-f', '--filename')

    args = parser.parse_args()
    
    if args.filename is not None:
        fh = open(args.filename, 'rb')
        b64c = fh.read()
        fh.close()
        
        print( base64encode( b64c ) )
        exit(0)       

    string_decode_or_encode = ""
    if type(args.string_decode_or_encode) == type([]):
        string_decode_or_encode = " ".join(args.string_decode_or_encode)
    
    print( base64encode( string_decode_or_encode ) )
