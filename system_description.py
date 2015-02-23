"""
# Info

- This contains description on where stuff is on the system.

# TODO:

- Put in private data file info:
    - Obviously, just use this for low security stuff (such as added layer of security when sending as mail), passwords for accounts I do not care about, ...
    - Always keep old key, but in comment (disable script using them).
    - Keep key indication in backup name.
"""

import os
import json
import pathlib

# Stick this into every file that is auto-generated. This is used for cleanup /
# allowing to remove the old files when a new set of files is created.
magic_tag_intstr = '4452669129437275268177914375'

def getPrivateDataFile():
    """
    This is a special file with special lookup logic.
    """
    
    cp = pathlib.Path(os.path.realpath(__file__))

    while not cp.parents[0].joinpath('private_data').is_file():
        cp = cp.parents[0]

    return cp.parents[0].joinpath('private_data').as_posix()

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
        file_template = file_template.replace('__custom__', "python3.4 ""__py_file__"" __opt_cmd__ $@")
    else:
        raise Exception("Not coded for os: %s." % os.name)

    return (file_ext, output_dir, file_template)

def __loadPrivateFile():

    fh = open(getPrivateDataFile(), 'r')
    jr = fh.read()
    fh.close()

    jd = json.loads(jr)

    return jd

def getFilesMap():
    jd = __loadPrivateFile()
    jd = jd['namedLocationMap']
    dirsMap = jd[os.name]
    dirsMap['private_data'] = getPrivateDataFile()
    return dirsMap

# This will add all the variables declared in the JSON file as local variables.
# This way, private_data.variable is accessible after importing the module.
jd = __loadPrivateFile()
localsDir = locals()
for k, v in jd['variables'].items():
    localsDir[k] = v

if __name__ == '__main__':
    #dm = getFilesMap()
    print(getPrivateDataFile())
