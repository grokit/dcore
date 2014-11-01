
import argparse

_meta_shell_command = 'k12'


def lineToASCII(line):
    
    #print(line[0:2])
    if line[0:2] == '|0':
        line = line[2:].strip(' |\r\n')
    else:
        return None
    
    lhex = line.split('|')
    
    lascii = []
    nhex = -1
    for hx in lhex:
        nhex += 1
        
        # Cut all bytes before the 42th (UDP).
        #if nhex < 42:
        #    continue
        
        i = int(hx, 16)
        
        if i < 32 or i > 126:
            i = ord('_')
        
        lascii.append( chr(i) )
    
    #print(lascii)
    
    return "".join(lascii)
    

if __name__ == '__main__':
    
    print('begin')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('filein', nargs='+')
    args = parser.parse_args()
    
    file_in = args.filein[0]
    
    fh = open(file_in, 'r')
    lines = fh.readlines()
    fh.close()
    
    allPayloads = []
    i = 0
    for line in lines:
        
        try:
            lineo = lineToASCII(line)
            
            if lineo is not None:
                allPayloads.append(lineo)
        except Exception as e:
            print('Failed line %s: %s. E: %s.' % (i, line, e))
        
        i += 1
    
    fh = open(file_in + '.k12bytes.txt', 'w')
    fh.write("\n".join(allPayloads))
    fh.close()
    
    print('end')
    