#!/usr/bin/python3

"""
One-run install of `dcore`.

# TODO
- If new bashrc, have a list of my stuff I want on every new computer and write from here.


"""

import sys
import os
import platform

def getBashrcOrEquivalent():
    """
    https://apple.stackexchange.com/questions/51036/what-is-the-difference-between-bash-profile-and-bashrc
    """
    if platform.system() in ["macosx", "Darwin"]:
        return os.path.expanduser('~/.bash_profile')
    else:
        return os.path.expanduser('~/.bashrc')

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

    fname = getBashrcOrEquivalent()

    with open(fname, 'r') as fh:
        file = fh.read()
        if not tag in file:
            file = bash_rc + '\n\n' + file
            open(fname, 'w').write(file)
        else:
            print('Warning: skipping writing new `%s` since it looks like tag is already present.' % fname)

    cmd = '. %s' % fname
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
    Goes to the end of file if already exist and no mark already.

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

    # If path to filename does not exist, create.
    folder = os.path.split(filename)[0]
    if not os.path.exists(folder):
        os.makedirs(folder)

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

# append to the history file, don't overwrite it
shopt -s histappend

# After each command, save and reload history
# https://unix.stackexchange.com/questions/1288/preserve-bash-history-in-multiple-terminal-windows
export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"

# Infinite history
# https://stackoverflow.com/questions/9457233/unlimited-bash-history
HISTSIZE=""
HISTFILESIZE=""

## Misc

# vim edit mode in bash. -> put in .inputrc if want available in other GNU tools.
# set editing-mode vi
# Following one is for .bashrc
set -o vi

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize
"""
    fname = getBashrcOrEquivalent()
    updateFileContentBetweenMarks(
            os.path.expanduser(fname), 
            '# DCORE_SECTION_BEGIN_8ygmfmsu926z06ym', 
            '# DCORE_SECTION_END_8ygmfmsu926z06ym', 
            CONTENT)

def setupI3():
    CONTENT = """
# me ======
bindsym $mod+Control+q exec i3lock -c 000000 # like macosx
#bindsym $mod+p exec i3lock -c 000000
exec --no-startup-id xss-lock -- i3lock -c 000000
exec xautolock -time 1

# Pulse Audio controls
bindsym XF86AudioRaiseVolume exec --no-startup-id pactl set-sink-volume 0 +5% #increase sound volume
bindsym XF86AudioLowerVolume exec --no-startup-id pactl set-sink-volume 0 -5% #decrease sound volume
bindsym XF86AudioMute exec --no-startup-id pactl set-sink-mute 0 toggle # mute sound

# # Sreen brightness controls
bindsym XF86MonBrightnessUp exec nux high
bindsym XF86MonBrightnessDown exec nux low

# me (end) ======
"""
    updateFileContentBetweenMarks(
            os.path.expanduser('~/.config/i3/config'), 
            '# DCORE_SECTION_BEGIN_8ygmfmsu926z06ym', 
            '# DCORE_SECTION_END_8ygmfmsu926z06ym', 
            CONTENT)

def setupVi():
    CONTENT = """
syntax on
filetype indent plugin on
" show existing tab with 4 spaces width
set tabstop=4
" " when indenting with '>', use 4 spaces width
set shiftwidth=4
" " On pressing tab, insert 4 spaces
set expandtab

" F2: compile and run current file.
autocmd FileType python nnoremap <F2> :w!<cr>:exec '!python3' shellescape(@%, 1)<cr>
autocmd FileType go nnoremap <F2> :w!<cr>:!go run %<cr>
autocmd FileType java nnoremap <F2> :w!<cr>:!javarun %<cr>
autocmd FileType cpp nnoremap <F2> :w!<cr>:!cpprun %<cr>

" F3: format current file.
autocmd FileType go nnoremap <F3> :w!<cr>:!go fmt %<cr>:e<cr>
autocmd FileType java nnoremap <F3> :w!<cr>:!astyle % --indent=spaces<cr>:e<cr>
autocmd FileType python nnoremap <F3> :w!<cr>:!autopep8 --in-place --aggressive --aggressive %<cr>:e<cr>

" F4: git commit.
nnoremap <F4> :!gitpp<cr>

" some extension added other command that starts with E.
" make it explicit here what I intend by E
command! E Explore

":set spell spelllang=en_us
":set nospell
"""
    updateFileContentBetweenMarks(
            os.path.expanduser('~/.vimrc'), 
            '" DCORE_SECTION_BEGIN_8ygmfmsu926z06ym', 
            '" DCORE_SECTION_END_8ygmfmsu926z06ym', 
            CONTENT)

def setupTmux():
    CONTENT = """
# set -g mode-mouse on
set -g mouse on
set -g status-bg colour17
set -g status-fg colour38
set-window-option -g mode-keys vi
"""
    updateFileContentBetweenMarks(
            os.path.expanduser('~/.tmux.conf'), 
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
    setupI3()
    setupVi()
    setupTmux()

