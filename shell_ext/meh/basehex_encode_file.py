
import base64
import argparse

_meta_shell_command = 'bhexf -s'

def baseHexencodeFile(str):
    fh = open(str, 'rb')
    fbytes = fh.read()
    fh.close()
    
    hexStr = []
    for byte in fbytes:
        hexT = hex(byte).replace('0x', '')
        if len(hexT) == 1: hexT = '0' + hexT
        hexStr.append( hexT )
    
    return "".join(hexStr)
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--string_decode_or_encode', nargs='+')

    args = parser.parse_args()

    string_decode_or_encode = ""
    if type(args.string_decode_or_encode) == type([]):
        string_decode_or_encode = " ".join(args.string_decode_or_encode)
    
    print( baseHexencodeFile( string_decode_or_encode ) )
    