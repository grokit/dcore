"""

BUGS

- the -f doesn't work
- should be 'do on text', with a special option if want to check it is a file

IMPROVEMENTS

- !! separate in two applications: 
    1. take the output of a command and execute something (doo: do_on_output.py)
    2. juice_files.py: take the output of a command, extract all the possible files & check if there are really files & print fullpath
    3. dof = doo + juice
- "-l" --> just do on last item
- allow inferring %file is not present (&warn)

- Allow more generic 'do on pattern', for which 'do on file' is more restricted case
- Allow just loging the output of the commands
"""

_meta_shell_command = 'dof'

import sys
import os
import subprocess
import stat
import argparse
import codecs

verbose = True

def log(msg):
    if verbose:
        print(msg)

def isDataSentToScript():
    mode = os.fstat(0).st_mode
    if stat.S_ISFIFO(mode):
         # stdin is piped
         return True
    elif stat.S_ISREG(mode):
         # stdin is redirected
         return True
    else:
         return False

def getStdinData():
    return codecs.getwriter('utf-8')(sys.stdin).read()
    #return sys.stdin.read() 

    
def aiTryJuiceFileFromFuzzyLine(str):
    """
    Try to return the file in cases where:
        c:\folder\file.txt some garbage here
        some garbage here c:\folder\file.txt
    """
    
    # Assume easy cases are already handled
    assert not os.path.isfile(str.strip())
    
    parts = str.split(' ')
    
    # Assumes there is no space in the path
    pot = []
    for part in parts:
        part = part.strip()
        if os.path.isfile(part):
            pot.append(part)
    
    if len(pot) == 1:
        return pot[0]
    
    # Could also try to pattern match for [a-z]:.*\.[az09...]
    
    return None
    
def aiTryToJuiceAllPossibleFiles(str):    
    
    files = []
    for line in str.splitlines():
        if os.path.isfile(line.strip()):
            files.append(line.strip())
            continue
        else:
            file = aiTryJuiceFileFromFuzzyLine(line)
            if file is not None:
                files.append(file)        
    
    #fh = open(r't:\temp\dof.txt', 'w')
    #fh.write("\r\n".join(files))
    #fh.close()
    
    return files
    
def extractFilelistFromStrList(str):
    """
    Try its best to recognize the format of the file list.
    
    What should ALWAYS work is single file on one line, e.g:
    file1.abc
    file 2.abc
    f i l e             3.abc.def
    [...]
    """
    lst = []
    for line in str.splitlines():
        if os.path.isfile(line.strip()):
            lst.append(line.strip())
            continue
    return lst
    
def extractFilelistFromFileOfStrList(file):
    log("extractFilelistFromFileOfStrList")
    fh = open(file, 'r', encoding='utf8')
    str = fh.read()
    fh.close()
    
    return str
    
FILE_MARKER = '%file'

def lstToStr(lst):
    
    str = []
    for l in lst:
        str.append(" " * 0 + l + "\r\n")
    
    return "".join(str)
    
def do():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('command', nargs='+')
    parser.add_argument('-f', '--filelist_file')
    parser.add_argument('-m', '--magic_juice', action="store_true")
    parser.add_argument('-v', '--verbose', type=int)
    
    args = parser.parse_args()
    
    global verbose
    if args.verbose is not None:
        verbose = args.verbose
    
    log(args)
        
    assert args.command is not None
    command = " ".join(args.command)
    filelist_file = args.filelist_file
    
    if command == 'np':
        command = 'start /b np'
    
    if not FILE_MARKER in command:
        log('Warning: %s not in command, appending at the end' % FILE_MARKER)
        command += " " + FILE_MARKER
    assert FILE_MARKER in command
    
    filesStr = ''
    if isDataSentToScript():
        filesStr = getStdinData()
        assert filelist_file is None
        log("Using stdin data:\n" + filesStr)
    else:
        assert filelist_file is not None
        filesStr = extractFilelistFromFileOfStrList(filelist_file)
        log("Using file data:\n" + filesStr)
    
    #log(filesStr)
    elLst = extractFilelistFromStrList(filesStr)
    magicLst = aiTryToJuiceAllPossibleFiles(filesStr)
    log("files extracted:\r\n%s" % lstToStr(elLst))
    
    if len(magicLst) > 0:
        log("magic files extracted:\r\n%s" % lstToStr(magicLst))
        if args.magic_juice is True:
            elLst = elLst + magicLst
    
    fileLst = []
    for el in elLst:
        if os.path.isfile(el):
            fileLst.append(el)
        else:
            # @@todo have a different log level for this, ALWAYS log
            log('Skipping: %s, not a file.' % el)
    
    for file in fileLst:
        cmd = command.replace(FILE_MARKER, '"' + file + '"')
        log("Executing: '%s'" % cmd)
        
        os.system(cmd)
        """
        rc = subprocess.call(cmd)
        if rc is not 0:
            log('Warning: executed program returned value: %s' % rc)
        """

if __name__ == '__main__':
    do()
        
