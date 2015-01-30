
import os
import os

_meta_shell_command = 'nuxui'

if __name__ == '__main__':
    cmd = 'sudo /etc/init.d/lightdm start'
    print(cmd)
    os.system(cmd)
