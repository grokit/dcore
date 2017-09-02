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

    fname = os.path.expanduser('~/.profile')
    if not os.path.isfile(fname):
        print('Could not find %s, trying .bashrc.' % fname)
        fname = os.path.expanduser('~/.bashrc')

    if not os.path.isfile(fname):
        print('Could not find %s, creating.' % fname)
        with open(fname, 'w') as fh:
            fh.write('\n')

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
    lines = [begin, '\n', content, end, '\n'] + lines

    with open(filename, 'w') as fh:
        for l in lines:
            fh.write(l)

def setupBashRc():
    CONTENT = """# Alias
alias cclip='xclip -selection clipboard'
alias clipp='xclip -selection clipboard -o'
alias youtube_mp3='youtube-dl --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" '

## Tmux Saves History Properly

# append history entries..
shopt -s histappend
# After each command, save and reload history
export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"
# Infinite history
HISTSIZE=100000000 HISTFILESIZE=100000000

## Misc

# vim edit mode in bash. -> put in .inputrc if want available in other GNU tools.
# set editing-mode vi
# Following one is for .bashrc
set -o vi
"""
    updateFileContentBetweenMarks(
            os.path.expanduser('~/.bashrc'), 
            '# DCORE_SECTION_BEGIN_8ygmfmsu926z06ym', 
            '# DCORE_SECTION_END_8ygmfmsu926z06ym', 
            CONTENT)

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



