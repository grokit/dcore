
import base64
import binascii # https://docs.python.org/3.4/library/binascii.html
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
    parser.add_argument('--filename_bytes', help = "Read filename and interpret bytes-str as direct bytes.")

    args = parser.parse_args()
    
    if args.filename is not None:
        fh = open(args.filename, 'rb')
        b64c = fh.read()
        fh.close()
        
        print( base64encode( b64c ).decode() )
        exit(0)       
    
    if args.filename_bytes is not None:
        raise Exception("Not done.")
        
    string_decode_or_encode = ""
    if type(args.string_decode_or_encode) == type([]):
        string_decode_or_encode = " ".join(args.string_decode_or_encode)
    
    print( base64encode( string_decode_or_encode ) )
