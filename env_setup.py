
import os
import platform

def getBashrcOrEquivalent():
    """
    https://apple.stackexchange.com/questions/51036/what-is-the-difference-between-bash-profile-and-bashrc
    """
    if platform.system() in ["macosx", "Darwin"]:
        return os.path.expanduser('~/.bash_profile')
    else:
        return os.path.expanduser('~/.bashrc')

def updateFileContentBetweenMarks(filename, begin, end, content, createOnMissing=True):
    """
    Use this script to update part of files between mark.
    Goes to the end of file if already exist and no mark already.

    For example:

    MyFile.txt:

        Something.

        BEGIN
        theBird=12
        END

        Something else.

    update('MyFile.txt', 'BEGIN', 'END', 'theBird=14')
    Would update everything between the begin and end marker with the string provided as the last parameter.
    """

    # If path to filename does not exist, create.
    if createOnMissing:
        folder = os.path.split(filename)[0]
        if not os.path.exists(folder):
            os.makedirs(folder)

    if not os.path.isfile(filename):
        print('Could not find %s, creating.' % filename)
        with open(filename, 'w') as fh:
            fh.write('\n')

    with open(filename, 'r') as fh:
        lines = fh.readlines()

    iBegin = -1
    iEnd = -1
    for i, l in enumerate(lines):
        if begin == l.strip():
            assert iBegin == -1
            iBegin = i
        if end == l.strip():
            assert iBegin != -1
            assert iEnd == -1
            iEnd = i

    if iBegin != -1 and iEnd > iBegin:
        lines = lines[0:iBegin] + lines[iEnd+1:]
    lines = lines + ['\n', begin, '\n', content, end, '\n']

    with open(filename, 'w') as fh:
        for l in lines:
            fh.write(l)

