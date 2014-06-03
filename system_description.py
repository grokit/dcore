"""
Defines where is what (files, applications, folders) in your system.

Obviously, personalize this to reflect your system / env.
"""

import os

# Stick this into every file that is auto-generated. This is used for cleanup / 
# allowing to remove the old files when a new set of files is created.
magic_tag_intstr = '4452669129437275268177914375'

def getDirsMap():
    if os.name == 'posix':
        dirsRepo = {
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
        dirsRepo = {
                'scripts':   r'c:\david\sync\scripts',
                'scriptsp':  r'c:\david\sync\scripts-private',
                'root':      r'C:\david\sync\dev',
                'dev':       r'C:\david\sync\dev',
                'desktop':   r'C:\Users\dgaulin\Desktop',                
        }
    else:
        raise Exception("Not coded for os: %s." % os.name)
    
    return dirsRepo

def getFilesMap():
    if os.name == 'posix':
        fileMap = {'todo':     '/home/david/Desktop/Dropbox/logs/Todo_Home.txt',
                   'ta':       '/home/david/Desktop/Dropbox/logs/TheArchive.txt',
                   'someday':  '/home/david/Desktop/Dropbox/logs/MaybeSomeday.txt'}
    elif os.name == 'nt':
        fileMap = {
                'todo':         r'c:\david\sync\scripts\todo.txt',
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
