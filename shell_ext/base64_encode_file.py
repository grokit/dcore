
import base64
import argparse

_meta_shell_command = 'b64f -s'

def base64encodeFile(str):
    fh = open(str, 'rb')
    fbytes = fh.read()
    fh.close()
    
    return base64.b64encode(fbytes)
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--string_decode_or_encode', nargs='+')

    args = parser.parse_args()

    string_decode_or_encode = ""
    if type(args.string_decode_or_encode) == type([]):
        string_decode_or_encode = " ".join(args.string_decode_or_encode)
    
    print( base64encodeFile( string_decode_or_encode ) )
    