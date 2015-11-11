"""
# TODO

## As

- Wrap inside dcore.data and put in a less prominent directory.

## Bs

- Put in private data file info:
    - Obviously, just use this for low security stuff (such as added layer of security when sending as mail), passwords for accounts I do not care about, ...
    - Always keep old key, but in comment (disable script using them).
    - Keep key indication in backup name.
"""

import os
import json
import pathlib
import platform

import dcore.data as data

# Stick this into every file that is auto-generated. This is used for cleanup /
# allowing to remove the old files when a new set of files is created.
magic_tag_intstr = 'GeneratedBy_%s_bg0sn9gtmq2jjper' % __file__

def getPrivateDataFilename():
    """
    This is a special file with special lookup logic.
    Logic is that we start where this script it, then bubble up to root until we find 'private_data'. 
    Like how .git repositories are found.
    """
    
    return os.path.join(data.dcoreData(), "private_file_v2")
    """
    cp = pathlib.Path(os.path.realpath(__file__))

    while not cp.parents[0].joinpath('private_data').is_file():
        cp = cp.parents[0]

    return cp.parents[0].joinpath('private_data').as_posix()
    """

def getAutogenFileTemplate():

    magic_tag = 'Magic number for easy deletion: %s.' % magic_tag_intstr

    file_template = r"""
    @rem Automatically created by '%s', do not modify.
    @rem %s

    __custom__

    """ % (os.path.normpath(__file__), magic_tag)

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
        output_dir = data.pathExt()
        file_template = file_template.replace('__custom__', "python ""__py_file__"" __opt_cmd__ %*")

    elif os.name == 'posix':
        file_ext = ''
        output_dir = '/usr/local/bin'
        file_template = file_template.replace('__custom__', "python3.4 ""__py_file__"" __opt_cmd__ $@")
    else:
        raise Exception("Not coded for os: %s." % os.name)

    return (file_ext, output_dir, file_template)

def __loadPrivateFile():

    if os.path.isfile(getPrivateDataFilename()):
        fh = open(getPrivateDataFilename(), 'r')
        jr = fh.read()
        fh.close()

        jd = json.loads(jr)
    else:
        print('Warning: cannot find private file %s.' % getPrivateDataFilename())
        jr = "{}"

    return json.loads(jr)

def __expandEnvVars(D):
    r"""
    %userprofile%: c:\users\userid
    $var: an_env_variable_expanded
    """
    return {k:os.path.expandvars(v) for (k, v) in D.items()}
    
def getFilesAndFoldersMap():
    jd = __loadPrivateFile()

    if 'namedLocationMap' in jd.keys():
        jd = jd['namedLocationMap']
        D = jd[os.name]
        D['private_data'] = getPrivateDataFilename()
        
        items = __expandEnvVars(D).items()
        for k,v in items:
            if not (os.path.isfile(v) or os.path.isdir(v)):
                st = "Warning: not file or dir: %s." % v
                print(st)
                #raise Exception(st)
        
        return {k:v for (k,v) in items}
    else:
        return {}

# @@bug BAN THIS. This is way to magicky.
# This will add all the variables declared in the JSON file as local variables.
# This way, system_description.variable is accessible after importing the module.
# Could relegate this as private.py and ONLY be used for passwords and the such ... but need to explain in exception when not found that this is data the user needs to set.
jd = __loadPrivateFile()
localsDir = locals()
if 'variable' in jd.keys():
    if jd['variable'] != Null:
        for k, v in jd['variables'].items():
            localsDir[k] = v

if __name__ == '__main__':
    #dm = getFilesAndFoldersMap()
    print(getPrivateDataFilename())
