
import base64
import argparse

_meta_shell_command = 'bhexd -s'

def baseHexDecodeStr(str):
    
    bytesa = []
    for i in range(0, len(str), 2):
        #print(str[i:i+2])
        bytesa.append( bytes.fromhex(str[i:i+2]) )
    
    #print(bytesa)
    return b"".join(bytesa)
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--string_decode_or_encode', nargs='+')

    args = parser.parse_args()

    string_decode_or_encode = ""
    if type(args.string_decode_or_encode) == type([]):
        string_decode_or_encode = " ".join(args.string_decode_or_encode)
    
    bt = baseHexDecodeStr( string_decode_or_encode )
    print( bt )
    
    fh = open('out.txt', 'wb')
    fh.write(bt)
    fh.close()
    