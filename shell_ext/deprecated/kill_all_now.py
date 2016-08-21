
import os
import argparse
import platform

_meta_shell_command = 'kk'
   
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('process_name')
    args = parser.parse_args()
    
    if platform.system().lower() == "windows":
        cmd = 'taskkill /im %s* /f' % args.process_name
    else:
        cmd = 'killall %s -9' % args.process_name
    
    print(cmd)
    os.system(cmd)

    
