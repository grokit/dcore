"""
One-run install of DCORE.

# TODO

- Do not rely on private_data so much... can know where dcore is without that.
"""

import sys
import os

if __name__ == '__main__':
    magicMark = "# Magic dcore tag: fh89h98h3f9hf39hf98ahsfd9djh." 
    dcoreLoc = os.path.split(os.path.realpath(__file__))[0]
    ppathMod = 'export PYTHONPATH=$PYTHONPATH:%s' % dcoreLoc
    os.system(ppathMod)
    profileF = os.path.expanduser('~/.profile')
    profile = open(profileF).read()
    if magicMark not in profile:
        profile = magicMark + "\n" + ppathMod + "\n" + profile
        open(profileF, 'w').write(profile)

    import system_setup.create_python_scripts_shortcuts
    system_setup.create_python_scripts_shortcuts.do()

    import system_setup.create_directories_shortcuts
    create_directories_shortcuts.do()
