
import os
import shutil

_meta_shell_command = 'docxtomd'

def fileReplace(fin, fout, rdict):

    fh = open(fin, 'r')
    lout = []
    for l in fh.readlines():
        print(l)
        for k in rdict:
            l = l.replace(k, rdict[k])
        lout.append(l)

    fh = open(fout, 'w')
    for l in lout:
        fh.write(l)

if __name__ == '__main__':

    files = os.listdir('.')
    files = [f for f in files if os.path.splitext(f)[1] == '.docx']

    assert len(files) == 1
    file = files[0]

    # Media is hardcoded to go in `media` after the path specified in --extract-media.
    fout = file.replace('.docx', '.md')
    cmd = 'pandoc -s %s -t markdown -s -o %s --extract-media .' % (file, fout)
    print(cmd)
    assert os.system(cmd) == 0

    # Markdown converter does not handle utf8 well.
    fileReplace(fout, fout, {'“': '"', '”': '"', "’":"'"})

    # Flatten media to current directory.
    mediaFolder = './media'
    files = [os.path.abspath(os.path.join(mediaFolder, f)) for f in os.listdir(mediaFolder)]

    for f in files:
        dst = os.path.split(f)[1]
        shutil.copy(f, dst)
    shutil.rmtree(mediaFolder)

    # Fix output markdown file
    fileReplace(fout, fout, {'./media/': './', r'\#': '#'})

    cmd = 'markdown %s > %s' % (fout, fout.replace('.md', '.html'))
    print(cmd)
    assert os.system(cmd) == 0

