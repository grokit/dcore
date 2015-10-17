
_meta_shell_command = 'ascii'

import sys
import argparse

ascii_annotation = '!!not-ascii!!'

def IsAscii(byteVal):
    return byteVal <= 127   
    
def forceToAscii(bytesVal, annotate=True):
    
    ob = []
    for b in bytesVal:
        if IsAscii(b):
            ob.append(int(b))
        else:
            if annotate:
                for x in [ord(x) for x in ascii_annotation]:
                    ob.append(x)
        
    return bytes(ob)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()

    parser.add_argument('files', nargs='+')
    parser.add_argument('-w', '--write_back', action="store_true")
    parser.add_argument('-n', '--no_annotation', action="store_true", default=False, help="Will not write the annotation in the output file in place of the non-ASCII characters.")
    
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
        asciiBytes = forceToAscii(fbytes, not args.no_annotation)
        
        fileOut = file + '.ascii'
        
        if args.write_back is True:
            fileOut = file
        
        fh = open(fileOut, 'wb')
        fh.write(asciiBytes)
        fh.close()    
        
        print('Wrote %s.' % fileOut)
