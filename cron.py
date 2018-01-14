import os
import stat
import getpass
import datetime

def install():
    fname = '/etc/cron.hourly/dcore_hourly.sh'
    user = os.environ['SUDO_USER']
    #cmd = 'su __user__ -c "python3 __file__ | tee ~/dcore_hourly.log"'
    cmd = "#!/bin/sh\nsu - arch -c '. ~/.bashrc && python3 __file__ |& tee ~/dcore_hourly.log'"
    cmd = cmd.replace('__file__', os.path.abspath(__file__))

    # If run under sudo, would get root
    # user = getpass.getuser()
    cmd = cmd.replace('__user__', user)

    print(cmd)
    with open(fname, 'w') as fh:
        fh.write(cmd)

    st = os.stat(fname)
    # https://docs.python.org/3/library/stat.html
    os.chmod(fname, st.st_mode | stat.S_IEXEC | stat.S_IXOTH)

def backup():
    import dcore.shell_ext.backup_remote as backup_remote
    backup_remote.do()

def mailTag():
    return "%s %s" % (datetime.datetime.now().isoformat(), 'm3pzBxlKu')

if __name__ == '__main__':
    if False:
        install()
    else:
        # Keep this here since root needs to install and won't be able to import.
        import dcore.apps.gmail.gmail as gmail
        import dcore.private_data as private_data
        print('Cron starting (stdout)')
        gmail.sendEmail(private_data.primary_email, "Cron starting " + mailTag(), "...")

        # List stuff to run.
        runme = [backup]

        for r in runme:
            try:
                r()
            except Exception as e:
                print('cron failed %s: %s.' % (r, e))

        gmail.sendEmail(private_data.primary_email, "Cron done " + mailTag(), "...")
