#!/usr/bin/python3

"""
One-run install of `dcore`.

# TODO
- If new bashrc, have a list of my stuff I want on every new computer and write from here.

ADD TMUX.conf

    set -g mode-mouse on
    set -g mouse-resize-pane on
    set -g mouse-select-pane on
    set -g mouse-select-window on
    ^^ does not work in Ubuntu :/
"""

import sys
import os
import platform

BASH_SETUP_FILE = ['~/.bash_profile']
BASH_STARTUP = ['~/.bashrc', '~/.profile']

def selectFirstExistingOrCreate(fname):
    if type(fname) is not type([]):
        raise Exception('Bad type: %s.' % type(fname))

    for f in fname:
        f = os.path.expanduser('~/.profile')
        if os.path.isfile(f):
            return f 

    # No file match, create the first in the list.
    f = os.path.expanduser(fname[0])
    with open(f, 'w') as fh:
        fh.write('\n')

    return f 

def setupShortcutsBootstrap():
    """
    We put all shortcuts in dcore-owned directory and add it to executable PATH loaded by shell.
    """

    # This import should be fine as it does not depend on path.
    import data

    tag = data.tagShortcutsForDeletion()
    home_scripts = os.path.abspath('../')

    shortcuts_folder = data.pathExt()

    bash_rc = """
# Magic dcore tag: %s_BEGIN.
export PYTHONPATH=$PYTHONPATH:%s
export PATH=$PATH:%s
# %s_END
    """ % (tag, home_scripts, shortcuts_folder, tag)

    bash_rc = bash_rc.replace('__home__', os.path.expanduser('~'))

    fname = selectFirstExistingOrCreate(BASH_STARTUP)

    with open(fname, 'r') as fh:
        file = fh.read()
        if not tag in file:
            file = bash_rc + '\n\n' + file
            open(fname, 'w').write(file)
        else:
            print('Warning: skipping writing new `%s` since it looks like tag is already present.' % fname)

    cmd = 'source %s' % fname
    print(cmd)
    os.system(cmd)

def setupShortcuts():
    create_python_scripts_shortcuts.do()

def delOld():
    folder = data.pathExt()

    tag = data.tagShortcutsForDeletion()
    files = [os.path.join(folder, f) for f in os.listdir(folder)]
    for file in files:
        with open(file, 'r') as fh:
            content = fh.read()

        if tag in content:
            print('Deleting %s.' % file)
            os.remove(file)

def tryImports():
    try:
        import dcore.data as data
        import dcore.create_python_scripts_shortcuts as create_python_scripts_shortcuts
        global data
        global create_python_scripts_shortcuts
        return True
    except ImportError as e:
        return False

def updateFileContentBetweenMarks(filename, begin, end, content):
    """
    Use this script to update part of files between mark.
    For example:

    MyFile.txt:

        Something.

        BEGIN
        theBird=12
        END

        Something else.

    update('MyFile.txt', 'BEGIN', 'END', 'theBird=14')
    Would update everything between the begin and end marker with the string provided as the last parameter.
    """
    if not os.path.isfile(filename):
        print('Could not find %s, creating.' % filename)
        with open(filename, 'w') as fh:
            fh.write('\n')

    with open(filename, 'r') as fh:
        lines = fh.readlines()

    iBegin = -1
    iEnd = -1
    for i, l in enumerate(lines):
        if begin == l.strip():
            assert iBegin == -1
            iBegin = i
        if end == l.strip():
            assert iBegin != -1
            assert iEnd == -1
            iEnd = i

    if iBegin != -1 and iEnd > iBegin:
        lines = lines[0:iBegin] + lines[iEnd+1:]
    lines = lines + ['\n', begin, '\n', content, end, '\n']

    with open(filename, 'w') as fh:
        for l in lines:
            fh.write(l)

def setupBashRc():
    CONTENT = """
    
## Alias

# pipe data to clipboard, e.g. cat <file> | cclip
alias cclip='xclip -selection clipboard'
alias clipp='xclip -selection clipboard -o'

alias youtube_mp3='youtube-dl --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" '

alias gg='gnome-open'

## Tmux Saves History Properly

# append history entries..
shopt -s histappend

# After each command, save and reload history
# https://unix.stackexchange.com/questions/1288/preserve-bash-history-in-multiple-terminal-windows
export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"

# Infinite history
HISTSIZE=100000000 
HISTFILESIZE=100000000

## Misc

# vim edit mode in bash. -> put in .inputrc if want available in other GNU tools.
# set editing-mode vi
# Following one is for .bashrc
set -o vi

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize
"""
    fname = selectFirstExistingOrCreate(BASH_SETUP_FILE)
    updateFileContentBetweenMarks(
            os.path.expanduser(fname), 
            '# DCORE_SECTION_BEGIN_8ygmfmsu926z06ym', 
            '# DCORE_SECTION_END_8ygmfmsu926z06ym', 
            CONTENT)

    STARTUP = """
. cdd
tmux
"""

    fname = selectFirstExistingOrCreate(BASH_STARTUP)
    updateFileContentBetweenMarks(
            os.path.expanduser(fname),
            '# DCORE_SECTION_BEGIN_lq71d2111iiiyyoeuq2xtild2428zxh7', 
            '# DCORE_SECTION_END_lq71d2111iiiyyoeuq2xtild2428zxh7', 
            STARTUP)

if __name__ == '__main__':

    if not tryImports():
        print('Not bootstrapped, ')
        print('Attempting to bootstrap. You may need to restart your terminal for changes to take effect.')
        setupShortcutsBootstrap()
        exit(0)

    data.createAllDirsIfNotExist()
    delOld()
    setupShortcuts()
    setupBashRc()

