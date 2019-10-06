
import os
import argparse

_meta_shell_command = 'media_video_compress'

def getArgs():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = getArgs()
    
    files_all = os.listdir('.')
    targets = set(['.mov'])
    files_all = [f for f in files_all if f[-4:] in targets]

    scale = '-vf scale=800:-1'
    #scale = ''
    cmd = 'ffmpeg -i {filename} {scale} -vcodec libx265 -crf 20 {output}.mp4'

    for filename in files_all:
        lcmd = cmd.format(filename=filename, scale=scale, output=os.path.splitext(filename)[0] + '_compressed')
        print(lcmd)
        os.system(lcmd)

