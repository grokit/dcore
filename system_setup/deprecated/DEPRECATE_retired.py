"""
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
        dirsMapPrivate = getFilesMap()
    except Exception as e:
        print("%s cannot get private directories: %s." % (__file__, e))
    dirsMap = dict(list(dirsMap.items()) + list(dirsMapPrivate.items()))

    return dirsMap
"""


"""    
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
"""