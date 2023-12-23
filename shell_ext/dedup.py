
import os
import datetime
import hashlib

SRCS = ['~/Downloads/0', '~/Downloads/1', '~/sync']
#SRCS = ['~/Downloads/0', '~/Downloads/1']

def get_all_files(rootdir='.'):
    F = []
    for dirpath, dirnames, fullpaths in os.walk(rootdir):
        for f in fullpaths:
            F.append(os.path.normpath(os.path.join(dirpath, f)))
    return F

class FileInfo:
    def __init__(self, fullpath, last_mod):
        self.fullpath = fullpath
        self.last_mod = last_mod

    def __repr__(self):
        return str(self.__dict__)

def extract_file_info(ff):
    gmtime = datetime.datetime.utcfromtimestamp(os.path.getmtime(ff))
    return FileInfo(fullpath=ff, last_mod=gmtime)

def filter_file(fullpath):
    return True

def dt_to_display(dt):
    return str(dt.isoformat())

if __name__ == '__main__':
    files = set()
    for src in SRCS:
        src = os.path.abspath(os.path.expanduser(src))
        files = files.union(set(get_all_files(src)))

    files = {ff for ff in files if filter_file(ff)}

    name_match = {}
    for ff in files:
        try:
            basename = os.path.basename(ff)
            if basename not in name_match:
                name_match[basename] = []
            name_match[basename].append(extract_file_info(ff))
        except Exception as ee:
            print(f'EXCEPTION: {ee}')

    for kk, same_name_files in name_match.items():
        if len(same_name_files) > 1:
            print('-'*60)
            for vv in same_name_files:
                filesize = os.path.getsize(vv.fullpath)
                fhash = 'skipped'
                if filesize < 1e6:
                    fhash = hashlib.new('md5', open(vv.fullpath, 'rb').read()).hexdigest()
                print(f'{kk}: last mod: {dt_to_display(vv.last_mod)}, hash: {fhash}, size: {filesize:08d}, {vv.fullpath}')
            print('-'*60)
