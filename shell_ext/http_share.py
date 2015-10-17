
import os

_meta_shell_command = 'http_share'

if __name__ == '__main__':
    # python2: python -m SimpleHTTPServer 8000
    os.system('python3 -m http.server 8000')
