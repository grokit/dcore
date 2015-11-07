"""
One-run install of DCORE.
"""

import sys
import os
import platform

if __name__ == '__main__':

    if patform.system() == "Windows":
        import system_setup.windows_path_set as windows_path_set
        pass
    
    import system_setup.create_python_scripts_shortcuts
    system_setup.create_python_scripts_shortcuts.do()

    #import system_setup.create_directories_shortcuts
    #create_directories_shortcuts.do()
