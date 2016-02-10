"""
One-run install of DCORE.

Open question: wether should copy all scripts to proper target dir as 'fire-and-forget' or try to adapt to where the data is (where the user puts it). 
Could save a file in ~/.dcore that points to where the repo is... but that would not work well for system path.
"""

# feh: change background
# diodon: clip
# pv: picture view
# scrot: screenshots i3
apt_get_packages = """
scrot
pv
feh
gparted
diodon
gimp
virtualbox-qt
p7zip-full
vim
git
i3
shutter
tmux
"""

tag = "fh89h98h3f9hf39hf98ahsfd9djh"
bash_rc = """
# Magic dcore tag: __tag__.
export PYTHONPATH=$PYTHONPATH:/home/arch/sync/scripts
export PATH=$PATH:/home/arch/sync/dcore_data/path_ext
""".replace('__tag__', tag)

import sys
import os
import platform

if __name__ == '__main__':
	doAptGet = True
	doPath = True 
	doShortcuts = True

	if doAptGet:
		for line in apt_get_packages.splitlines():
			if line.strip() != "":
				cmd = "sudo apt-get -y install %s" % line
				print(cmd)
				os.system(cmd)

	if doPath:
		bash_rc = bash_rc.replace('__home__', os.path.expanduser('~'))
		if platform.system() == "Windows":
			import system_setup.windows_path_set as windows_path_set
			windows_path_set.do()
		else:
			fname = os.path.expanduser('~/.bashrc')
			file = open(fname, 'r').read()
			if not tag in file:
				file = bash_rc + '\n\n' + file
				open(fname, 'w').write(file)

	if doShortcuts:
		import dcore.data as data

		data.createAllDirs()

		import system_setup.create_python_scripts_shortcuts
		system_setup.create_python_scripts_shortcuts.do()

		#import system_setup.create_directories_shortcuts
		#create_directories_shortcuts.do()
