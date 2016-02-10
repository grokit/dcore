"""
One-run install of DCORE.

Open question: wether should copy all scripts to proper target dir as 'fire-and-forget' or try to adapt to where the data is (where the user puts it). Could save a file in ~/.dcore that points to where the repo is... but that would not work well for system path.
"""

apt_get_packages = """
virtualbox-qt
p7zip-full
vim
git
i3
clipper
tmux
"""

import sys
import os
import platform

if __name__ == '__main__':
	for line in apt_get_packages.splitlines():
		if line.strip() != "":
			cmd = "sudo apt-get -y install %s" % line
			print(cmd)
			os.system(cmd)


"""
    if False and platform.system() == "Windows":
        import system_setup.windows_path_set as windows_path_set
        windows_path_set.do()

    import dcore.data as data

    data.createAllDirs()

    import system_setup.create_python_scripts_shortcuts
    system_setup.create_python_scripts_shortcuts.do()

    #import system_setup.create_directories_shortcuts
    #create_directories_shortcuts.do()
"""
