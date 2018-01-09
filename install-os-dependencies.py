#!/usr/bin/python3

"""
One-run install of Ubuntu dependencies.

## TODO

Save / restore files in user's root directory which defines how app work:
    - vim
    - i3
    - bashrc
    ---> see save_env script

# BUGS

- Now that path extention is in ~/.profile instead of ~/.bashrc, requires reboot after install. Why sourcing file not enough?
"""

import sys
import os
import platform

# astyle: inside VIM, `:%astyle` to format code
# macchanger: NOT enabled since at install it pops-open a menu :(
apt_get_packages = """
g++
astyle
xclip
p7zip-full
vim
git
tmux
ack-grep
openssh-server
mosh
atop
pdftk
silversearcher-ag
python3-matplotlib
clang-4.0
"""

# cmus: command-line music player
# feh: change background
# diodon: clip
# pv: picture view
# scrot: screenshots i3
apt_get_packages_extended = """
xautolock
valgrind
kcachegrind
pdfsam
cmus
xbacklight
scrot
pv
feh
gparted
gimp
eclipse-platform
i3
python-pip
calibre
mplayer2
keepass2
gitk
okular
python3-pip
blender
wkhtmltopdf
mit-scheme
clang-format
vlc
pinta
youtube-dl
inkscape
nmap
texlive-full
texmaker
duplicity
borgbackup
nethogs
ncdu
"""

apt_get_packages += apt_get_packages_extended

# pip3 install rsa?, https://stuvel.eu/rsa
apt_get_packages_removed = """
vlc-nox
diodon
monodevelop
mono-devel
guake
virtualbox-qt
shutter
"""

ssh_public_key = """ssh-rsa REMOVED
"""

def setupAptGet():
    for line in apt_get_packages.splitlines():
            if line.strip() != "":
                    cmd = "sudo apt-get -y install %s" % line
                    print(cmd)
                    os.system(cmd)

def setupPath():
    tag = "fh89h98h3f9hf39hf98ahsfd9djh"
    home_scripts = os.path.abspath('../')
    shortcuts_folder = os.path.abspath(os.path.expanduser('~/sync/dcore_data/path_ext')) # @@bug: should be able to adjust to where git checkout was done. other script puts in this folder
    bash_rc = """
# Magic dcore tag: %s.
export PYTHONPATH=$PYTHONPATH:%s
export PATH=$PATH:%s
    """ % (tag, home_scripts, shortcuts_folder)

    bash_rc = bash_rc.replace('__home__', os.path.expanduser('~'))
    if platform.system() == "Windows":
            import system_setup.windows_path_set as windows_path_set
            windows_path_set.do()
    else:
            fname = os.path.expanduser('~/.profile')
            file = open(fname, 'r').read()
            if not tag in file:
                    file = bash_rc + '\n\n' + file
                    open(fname, 'w').write(file)

    os.system('source ~/.profile')

def setupShortcuts():
    import dcore.data as data

    data.createAllDirsIfNotExist()

    import dcore.create_python_scripts_shortcuts
    dcore.create_python_scripts_shortcuts.do()

def setupSSH():
    raise "Disabled feature. Enable manually if you dare."

    dirr = os.path.expanduser('~/.ssh')
    if not os.path.exists(dirr):
        os.makedirs(dirr)

    fname = os.path.expanduser('~/.ssh/authorized_keys')

    print('Be careful, you are adding the default ssh public key to %s, which gives access to the owner of the associated private key to this computer. Make sure you review this change.' % fname)

    if os.path.isfile(fname):
        fh = open(fname, 'a')
    else:
        fh = open(fname, 'w')
    fh.write('\n')
    fh.write(ssh_public_key)
    fh.write('\n')
    fh.close()

    os.system('sudo restart ssh')
    os.system('sudo /etc/init.d/ssh restart')

if __name__ == '__main__':
    setupAptGet()
    #setupPath()
    #setupShortcuts()
    #setupSSH()

