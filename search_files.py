"""
"""
import os
import fnmatch

# Note: taken from a sub-script, not linked from anywhere, but could do refactor
# to do so as it's often what script need.
def getAllFiles(rootdir='.'):
    FF = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for ff in filenames:
            FF.append(os.path.normpath(os.path.join(dirpath, ff)))
    return FF

def getAllFilesRecursively(in_allowedExtensionsGlobList, in_RootDir='.'):
    """
    E.g.: getAllFilesRecursively(['*.txt'], './folder/to/files')
    E.g.: getAllFilesRecursively(['*.txt', '*.bat'])
    """
    #Allow user to call using both '*.txt' and ['*.txt']
    if (type(in_allowedExtensionsGlobList) == type('')):
        in_allowedExtensionsGlobList = [in_allowedExtensionsGlobList]
    assert (type([]) == type(in_allowedExtensionsGlobList))

    fileList = []
    for root, subFolders, files in os.walk(in_RootDir):
        for file in files:

            add = False
            for glob in in_allowedExtensionsGlobList:
                if fnmatch.fnmatch(file, glob):
                    add = True

            if add:
                fullPathFile = os.path.join(root, file)
                normalizedFullPath = os.path.abspath(fullPathFile)
                fileList.append(normalizedFullPath)

    # return: List of fullpath string to files matching extensions provided.
    return fileList


def filterFilesByExtension(lstFullPathFilenames, lstExtensionsToKeep):
    fileList = []
    for file in lstFullPathFilenames:
        add = False
        for glob in lstExtensionsToKeep:
            if fnmatch.fnmatch(os.path.split(file)[1], glob):
                add = True
        if add:
            fileList.append(file)
    return fileList
