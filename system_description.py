"""
# TODO: put in private data file info:
    - Obviously, just use this for low security stuff (such as added layer of security when sending as mail), passwords for accounts I do not care about, ...
    - Always keep old key, but in comment (disable script using them).
    - Keep key indication in backup name.
"""

import os
import json

# Stick this into every file that is auto-generated. This is used for cleanup / 
# allowing to remove the old files when a new set of files is created.
magic_tag_intstr = '4452669129437275268177914375'

def getDirsMap():
    
    #@@@todo-a: move to file
    
    if os.name == 'posix':
        dirsMap = {
                'dropbox':   '/home/david/Desktop/Dropbox',
                'scripts':   '/home/david/Desktop/Dropbox/scripts',
                'root':      '/media/75a94e19-dccf-477a-bd80-251f0231a0b1/data',
                'dev':       '/media/75a94e19-dccf-477a-bd80-251f0231a0b1/data/dev',
                'web':       '/media/75a94e19-dccf-477a-bd80-251f0231a0b1/data/dev/website',
                'archive':   '/media/75a94e19-dccf-477a-bd80-251f0231a0b1/data/archive',
                'pics':      '/media/75a94e19-dccf-477a-bd80-251f0231a0b1/data/archive/media_pers',                
                'downloads': '/home/david/Downloads',                
        }
    elif os.name == 'nt':
        dirsMap = {
        }
    else:
        raise Exception("Not coded for os: %s." % os.name)
    
    dirsMapPrivate = {}
    try:
        dirsMapPrivate = getDirsMapPrivate()
    except Exception as e:
        print("%s cannot get private directories: %s." % (__file__, e))
    dirsMap = dict(list(dirsMap.items()) + list(dirsMapPrivate.items()))
        
    return dirsMap

def getFilesMap():
    #@@@todo-a: move to file
    if os.name == 'posix':
        fileMap = {
                   'todo':     '/home/david/Desktop/Dropbox/logs/Todo_Home.txt',
                   'ta':       '/home/david/Desktop/Dropbox/logs/TheArchive.txt',
                   'python_private':       '/home/david/Desktop/Dropbox/scripts/private_data.py',
                   'someday':  '/home/david/Desktop/Dropbox/logs/MaybeSomeday.txt',
                   'private_data':  '/home/david/Desktop/Dropbox/scripts/private_data',
                   }
    elif os.name == 'nt':
        fileMap =  {
                'todo':         r'c:\david\sync\scripts\todo.txt',
                'private_data': r'c:\david\sync\scripts-private\private_data',
        }
    else:
        raise Exception("Not coded for os: %s." % os.name)
    
    return fileMap
    
def getAutogenFileTemplate():
    
    magic_tag = 'Magic number for easy deletion: %s.' % magic_tag_intstr
    
    file_template = r"""
    @rem Automatically created by '%s', do not modify.
    @rem %s

    __custom__

    """ % (__file__, magic_tag)
    
    if os.name == 'nt':
        pass
    elif os.name == 'posix':
        file_template = file_template.replace('@', '#')
    else:
        raise Exception("Not coded for os: %s." % os.name)
    
    return file_template

def getPythonScriptsEnv():
    
    file_template = getAutogenFileTemplate()
    
    if os.name == 'nt':
        file_ext = '.bat'
        output_dir = os.getcwd() + '\\path_ext'
        file_template = file_template.replace('__custom__', "python ""__py_file__"" __opt_cmd__ %*")
        
    elif os.name == 'posix':
        file_ext = ''
        output_dir = '/usr/local/bin'
        file_template = file_template.replace('__custom__', "python3 ""__py_file__"" __opt_cmd__ $@")
    else:
        raise Exception("Not coded for os: %s." % os.name)
    
    return (file_ext, output_dir, file_template)

def getWindowsAppStuff():
        
    APP_FOLDER = r'C:\david\sync\app'
    DEST_BATCH = r'C:\david\sync\launchers'
    
    # List the runnable applications that should be found under the system.
    # In Windows, those name + .exe should give the executable name.
    APPS = [
        r'launchy',
        r'ditto',
        r'notepad++',
        r'babaschess',
        r'brainworkshop',
        r'7zFM',
        r'blender',
        r'gimp-2.8',
        r'SkypePortable',
        r'console',
        r'pdfsam-starter',
        r'PDFXCview',
        r'SQLite Database Browser 2.0 b1',
        r'procexp',
        r'procmon',
        r'tcpview',
        r'ThunderbirdPortable',
        r'TimeForTea',
        r'TrueCrypt',
        r'uTorrent',
        r'VirtuaWin',
        r'vlc',
        r'windirstat',
        r'foobar2000',
        r'inkscape',
        r'calibre_rt',
        r'everything-portable',
        r'Greenshot',
        r'gvim',
        r'',
        ]

    BAT_TEMPLATE = r"""
    rem Automatically created by '%s', do not modify.
    rem Magic number for easy deletion: %s.
    start "__title__" "__launcher__"
    exit
    """ % (__file__, magic_tag_intstr)
    
def __loadPrivateFile():
    
    fileMap = getFilesMap()
    privateDataFile = fileMap['private_data']

    fh = open(privateDataFile, 'r')
    jr = fh.read()
    fh.close()
    
    jd = json.loads(jr)

    return jd

def getDirsMapPrivate():
    jd = __loadPrivateFile()
    jd = jd['dirs']
    dirsMap = jd[os.name]
    return dirsMap

# This will add all the variables declared in the JSON file as local variables.
# This way, private_data.variable is accessible after importing the module.
jd = __loadPrivateFile()
localsDir = locals()
for k, v in jd['variables'].items():
    localsDir[k] = v

if __name__ == '__main__':
    dm = getDirsMapPrivate()
    #print(dm)