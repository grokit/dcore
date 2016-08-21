
import os

_meta_shell_command = 'gite'

def getArgs():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = getArgs()
    print(args)

    cmd = []
    cmd.append('git add --all :/')
    cmd.append('git commit -a -m "++auto"')
    for c in cmd:
        print(c)
        os.system(c)
