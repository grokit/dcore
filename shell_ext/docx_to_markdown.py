
import os

_meta_shell_command = 'docxtomd'

if __name__ == '__main__':

    files = os.listdir('.')
    files = [f for f in files if os.path.splitext(f)[1] == '.docx']

    assert len(files) == 1
    file = files[0]

    cmd = 'pandoc -s %s -t markdown -o %s --extract-media media' % (file, file.replace('.docx', '.md'))
    print(cmd)
    os.system(cmd)

