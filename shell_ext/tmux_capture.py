
import os

_meta_shell_command = 'tmux_capture'
cmd = 'tmux capture-pane -S -300 && tmux save-buffer ~/screen.tmux'
print(cmd)
os.system(cmd)
