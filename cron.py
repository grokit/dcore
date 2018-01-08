import os
import stat
import getpass

def install():
    fname = '/etc/cron.hourly/dcore_hourly.sh'
    cmd = 'su __user__ -c "python3 __file__ | tee ~/dcore_hourly.log"'
    cmd = cmd.replace('__file__', os.path.abspath(__file__))

    user = os.environ['SUDO_USER']
    # If run under sudo, would bet root
    # user = getpass.getuser()

    cmd = cmd.replace('__user__', user)


    print(cmd)
    with open(fname, 'w') as fh:
        fh.write(cmd)

    st = os.stat(fname)
    # https://docs.python.org/3/library/stat.html
    os.chmod(fname, st.st_mode | stat.S_IEXEC | stat.S_IXOTH)

if __name__ == '__main__':

    #install()
    print('I EXEC')

