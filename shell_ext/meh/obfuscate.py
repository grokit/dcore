"""
Not completed. Do not use.
"""

import argparse
import base64
import binascii

_meta_shell_command = 'obfu '

key = 'hd8y49287t7yt89sjf0djf0924t8y489ytg98hdfkahf4870846yuhfsdhfq8fyu204uf'

def tryDecode(txt):

    O = []
    for i in range(0, len(txt), 2):
        print('i: %i' % i)
        v = txt[i:i+2]
        v = int(v, 16)
        v = ord(txt[i]) ^ ord(key[i])
        print(v)
        O.append( hex(v).split('x')[1] )
    
    dec = "".join(O)
    print(dec)
    r = base64.b16decode(dec)
    return r    

def getArgs():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('to_obfuscate', nargs='+')
    
    args = parser.parse_args()
    
    return args
    
if __name__ == '__main__':
    
    args = getArgs()
    print(args)
    
    txt = args.to_obfuscate
    if type(txt) == type([]):
        txt = " ".join(txt)
    
    res = None
    if txt[0] == '!':
        res = tryDecode(txt[1:])
    
    if res is not None:
        print(res)
        exit(0)
    
    while len(key) < len(txt):
        key = key + key
    key = key[0:len(txt)]
    
    O = []
    for i in range(0, len(txt)):
        v = ord(txt[i]) ^ ord(key[i])
        v = '%.2X' % v
        O.append( v )
    
    out = '!' + "".join(O)
    print(out)

    
