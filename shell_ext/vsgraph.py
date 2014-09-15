
import re
import sys
import os

import dcore.search_files as fsearch

_meta_shell_command = 'vsgraph'

class Node:
    pass

example_sys_var = os.environ['example_sys_var']
    
def refToFullPath(filepath, ref):
    ref = ref.strip()
    #print(ref)
    
    if ref.lower() == 'system' or ref.lower() == 'microsoft':
        return None
    if len(ref.split('.')) > 0 and (ref.split('.')[0].lower() == 'system' or ref.split('.')[0].lower() == 'microsoft'):
        return None
    
    ## TODO: generic replace with env with regex
    ref = ref.replace('$(example_sys_var)', example_sys_var)
    ref = ref.replace('$(example_sys_var)', example_sys_var)
    
    if ref[0] == '.' or ref[0] == '\\':
        ref = os.path.join(filepath, ref)
    
    ref = os.path.abspath(ref)
    
    #print(os.path.exists(ref))
    if not os.path.exists(ref):
        errm = "%s does not exist." % ref
        #raise Exception(errm)
        print(errm)
        return None
    
    return ref
    
def toGraph(filesToRefs, fout):
    
    template = """
digraph G {
__insert_here__
}    
    """
    
    glines = []
    #print(filesToRefs)
    for file, ref in filesToRefs:
        
        #file = file.split('\\')[-1]
        #ref = ref.split('\\')[-1]
        
        glines.append("%s -> %s;\n" % (file, ref))
    
    template = template.replace('__insert_here__', "".join(glines))
    
    template = template.replace('\\', '_')
    template = template.replace('.', '_')
    template = template.replace(':', '_')
    
    fh = open(fout, 'w')
    fh.write(template)
    fh.close()
    
def filter(fileToRefs, fVA):
    fileToRefsO = []
    
    for file, epath in fileToRefs:
        isAdd = False
        
        for fV in fVA:
            if fV in file or fV in epath:
                isAdd = True
        
        if isAdd:
            fileToRefsO.append( (file, epath) )
    
    #print(fileToRefsO)
    return fileToRefsO
    
def sSearch(tDict, va):
    
    rv = tDict[va]
    parts = va.split(os.sep)
    for i in range(2, len(parts)):
        if "_".join(parts[-i:]) not in tDict:
            rv = "_".join(parts[-i:])
            break
    return rv
    
def simplify(fileToRefs):
    fileToRefsO = []
    
    tDict = {}
    for file, epath in fileToRefs:
        tDict[file] = file
        tDict[epath] = epath
    
    for file, epath in fileToRefs:
        fr = sSearch(tDict, file)
        tDict[file] = fr
        
        fr = sSearch(tDict, epath)
        tDict[epath] = fr        
    
    for file, epath in fileToRefs:
        
        fileToRefsO.append( (tDict[file], tDict[epath]) )
        
    #print(fileToRefsO)
    return fileToRefsO
    
def juiceRefs(file):
    #print(file)
    file = os.path.abspath(file)
    
    fh = open(file, 'r')
    lines = fh.readlines()
    fh.close()
    
    fileToRefs = []
    pattern = r'.*ProjectReference.*?"(.*)".*'
    repl = r'\1'    
    
    filepath = os.path.split(file)[0]
    
    for line in lines:
        if re.search(pattern, line):
            lnout = re.sub(pattern, repl, line)
            #print(line)
            #print(lnout)        
            epath = refToFullPath(filepath, lnout)
            #print(epath)
            if epath is not None:
                fileToRefs.append( (file, epath) )
    
    return fileToRefs
    
    
if __name__ == '__main__':
    files = fsearch.getAllFilesRecursively('*.*proj', '.')
    
    fileToRefs = []
    for file in files:
        fileToRefs += juiceRefs(file)
    
    fileToRefs = filter(fileToRefs, ['cxncore', 'cs.vcxproj'])
    fileToRefs = simplify(fileToRefs)
    
    fout = 'out.dot'
    toGraph(fileToRefs, fout)
    
    cmd = r'C:\david\sync\app\Graphviz2.36\bin\dot.exe -Tpng %s -o out.png' % fout
    print(cmd)
    os.system(cmd)
    
        
