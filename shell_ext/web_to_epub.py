import argparse
import tempfile
import os
import string

_meta_shell_command = 'web_to_epub'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('webpage', type=str)
    return parser.parse_args()


def dump_web_to_file(url):
    tempfile_fh =  tempfile.NamedTemporaryFile(delete=True, suffix='.html')
    cmd = f'wget --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36" -O {tempfile_fh.name} {url}'
    print(cmd)
    assert os.system(cmd) == 0
    return tempfile_fh

def pandoc_convert(filename_html, filename_out):
    cmd = f'pandoc {filename_html} -o {filename_out}'
    #cmd = f'ebook-convert {filename_html} {filename_out}'
    print(cmd)
    assert os.system(cmd) == 0

def url_to_filename(url):
    vv = []
    for cc in url:
        if cc not in string.ascii_lowercase + string.digits:
            vv.append('_')
        else:
            vv.append(cc)
    return "".join(vv)
    

def do():
    args = get_args()
    tempfile_fh = dump_web_to_file(args.webpage)
    pandoc_convert(tempfile_fh.name, url_to_filename(args.webpage) + '.epub')

if __name__ == '__main__':
	do()


