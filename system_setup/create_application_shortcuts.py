
r"""
# Startup:

C:\Users\(User-Name)\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup
"""

import os

import dcore.search_files as sfiles

def do():
    bins = sfiles.getAllFilesRecursively(['*.exe'], APP_FOLDER)
    
    lAPPS = [app.lower() + '.exe' for app in APPS]
    
    targets = {}
    for fpbin in bins:
        bin = os.path.split(fpbin)[1].lower()
        if bin in lAPPS:
            assert targets.get(bin) == None
            targets[bin] = fpbin
    
    for k, v in targets.items():
        target = os.path.join(DEST_BATCH, k.replace('.exe', '.bat'))
        bat_content = BAT_TEMPLATE.replace('__launcher__', v)
        bat_content = bat_content.replace('__title__', k)
        
        print('Creating %s.' % target)
        
        fh = open(target, 'w')
        fh.write(bat_content)
        fh.close()

if __name__ == "__main__":
    do()