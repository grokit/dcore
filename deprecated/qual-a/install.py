#!/usr/bin/python3

"""
One-run install of DCORE.

## TODO

Save / restore files in user's root directory which defines how app work:
    - vim
    - i3
    - bashrc

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
monodevelop
mono-devel
p7zip-full
vim
git
tmux
ack-grep
ack-grep
openssh-server
"""

# cmus: command-line music player
# feh: change background
# diodon: clip
# pv: picture view
# scrot: screenshots i3
apt_get_packages_extended = """
guake
cmus
xbacklight
scrot
pv
feh
gparted
gimp
virtualbox-qt
eclipse-platform
i3
shutter
silversearcher-ag
python-pip
kate
calibre
mplayer2
vlc-nox
keepass2
gitk
okular
"""

apt_get_packages_maybes_meh = """
"""

apt_get_packages += apt_get_packages_extended

apt_get_packages_removed = """
diodon
"""

ssh_public_key = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDfvvkTRv6R1EHvJ5BE9YIr/VUFpRpDRyZHGp/qSXcMGooNpAMEvtbLu6cNy4wGp6Gt0QbPnec4bTlwWmOfQH2E4k080yERIC+PcvDVkOTFpw1pCJ3iiisXJDrBnNqxgczX+no9bFVsyzrnQb2e8VNkXLNAvSRu/r93XSQmqQB04R+1fy2Uhbg8fzN/5WPnkTUZG/DpP1t4IfreAoOHt1wNbGbOatrLvsZ7iL86CE34MdXTko6koeZX/uILyuEJKSqTwc30Mzi6qZiPXTr1qKA2wbrQRm3K7TWGSHJcLJ0HMvWV8S9o7CoUa7aEtbKn3jDDfVE4dzLGsUVgnCpfJYV3 arch@arch-nx64
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

    data.createAllDirs()

    import system_setup.create_python_scripts_shortcuts
    system_setup.create_python_scripts_shortcuts.do()

    #import system_setup.create_directories_shortcuts
    #create_directories_shortcuts.do()

def setupSSH():

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
    #setupAptGet()
    setupPath()
    setupShortcuts()
    #setupSSH()

