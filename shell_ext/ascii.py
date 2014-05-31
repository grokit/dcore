
_meta_shell_command = 'ascii'

import sys
import argparse

def IsAscii(byteVal):
    return byteVal <= 127   
    
def forceToAscii(bytesVal):
    
    ob = []
    for b in bytesVal:
        if IsAscii(b):
            ob.append(int(b))
        else:
            ob.append(ord('@'))
            ob.append(ord('!'))
            ob.append(ord('@'))
            ob.append(ord('@'))
            ob.append(ord('@'))
            ob.append(ord('!'))
            ob.append(ord('@'))
    
    return bytes(ob)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()

    parser.add_argument('files', nargs='+')
    parser.add_argument('-w', '--write_back', action="store_true")
    
    args = parser.parse_args()
    
    files = args.files
    assert len(files) == 1
    file = files[0]
    
    fh = open(file, 'rb')
    fbytes = fh.read()
    fh.close()
    
    isAscii = True
    try:
        fbytes.decode('ascii')
    except:
        isAscii = False

    if isAscii:
        print('File %s is ascii.' % file)
    else:
        print('File %s not ascii, try to fix.' % file)
        asciiBytes = forceToAscii(fbytes)
        
        fileOut = file + '.ascii'
        
        if args.write_back is True:
            fileOut = file
        
        fh = open(fileOut, 'wb')
        fh.write(asciiBytes)
        fh.close()    
        
        print('Wrote %s.' % fileOut)
