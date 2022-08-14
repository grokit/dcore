
import os
import glob
import argparse
import shutil

_meta_shell_command = 'flatten_dir'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--apply', action="store_true", help='')
    return parser.parse_args()

def reduce_to_immediate(path):
    path_parts = path.split(os.sep)
    if len(path_parts) <= 1: return None
    rv = os.path.join(path_parts[0], path_parts[1])
    return rv

if __name__ == '__main__':
    args = get_args()
    files = list(glob.iglob('.' + '/**/*.**', recursive=True))
    files_mov = [(ff, os.path.split(ff)[1]) for ff in files]
    folders_rm = [reduce_to_immediate(os.path.split(ff)[0]) for ff in files]
    folders_rm = set([ff for ff in folders_rm if ff is not None])

    for ff, move_to in files_mov:
        assert not os.path.isfile(move_to)
    for ff, move_to in files_mov:
        assert not os.path.isfile(move_to)
        print(f'copy {ff} -> {move_to}')
        if args.apply:
            shutil.copy(ff, move_to)
    for folder in folders_rm:
        if folder is not None:
            print(f'rm -rf {folder}')
            if args.apply:
                shutil.rmtree(folder)
