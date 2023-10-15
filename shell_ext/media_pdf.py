"""
uuid:::811239781239273192873819231

Other tools:
- pdfarranger is really great at rotating and re-arranging pages.
    - sudo apt install pdfarranger
"""
import os
import argparse
import shutil

_meta_shell_command = 'media_pdf'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=str, nargs=1)
    parser.add_argument('file', type=str, nargs=1)
    parser.add_argument('-o', '--overwrite', action='store_true')
    parser.add_argument('--rotate_left', action='store_true', help='Otherwise, by default rotates right (clockwise).')
    args = parser.parse_args()
    return args

def _gen_output_file(input_file, marker):
    return os.path.splitext(input_file)[0] + marker + os.path.splitext(input_file)[1] 

def compress(args):
    input_file = args.file[0]
    output_file =  _gen_output_file(input_file, '_compressed')
    QUALITY = 'screen' # 72 dpi
    QUALITY = 'ebook' # 150 dpi
    CMD = f'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/{QUALITY} -dNOPAUSE -dQUIET -dBATCH -sOutputFile={output_file} {input_file}'

    print(CMD)
    os.system(CMD)
    if args.overwrite:
        shutil.move(output_file, input_file)

def rotate(args):
    input_file = args.file[0]
    MARKER = '_rotated'
    output_file =  _gen_output_file(input_file, '_rotated')
    rotation_dir = 'right'
    if args.rotate_left:
        rotation_dir = 'left'
    CMD = f'pdftk {input_file} cat 1-end{rotation_dir} output {output_file}'

    print(CMD)
    os.system(CMD)
    if args.overwrite:
        shutil.move(output_file, input_file)

def split(args):
    input_file = args.file[0]
    output_prefix =  os.path.splitext(_gen_output_file(input_file, '_split'))[0]
    CMD = f'pdftk {input_file} burst output {output_prefix}_%04d.pdf'
    print(CMD)
    os.system(CMD)

def join(args):
    output_file = args.file[0]
    CMD = f'pdftk *.pdf cat output {output_file}'
    print(CMD)
    os.system(CMD)

def grayscale(args):
    input_file = args.file[0]
    output_file =  _gen_output_file(input_file, '_grayscale')
    CMD = f' gs -sDEVICE=pdfwrite -sProcessColorModel=DeviceGray -sColorConversionStrategy=Gray -dOverrideICC  -o {output_file} -f {input_file}'
    print(CMD)
    os.system(CMD)

COMMANDS = {
        'compress': compress,
        'rotate': rotate,
        'split': split,
        'join': join,
        'grayscale': grayscale,
        }

if __name__ == '__main__':
    args = get_args()
    # This is not necessary, argparse marks those as required.
    assert args.file != None
    assert len(args.file) == 1
    assert args.mode != None
    assert len(args.mode) == 1
    if args.mode[0] in COMMANDS.keys():
        COMMANDS[args.mode[0]](args)
    else: raise Exception(f'bad command: {args.mode}. Available commands: {COMMANDS.keys()}.')







