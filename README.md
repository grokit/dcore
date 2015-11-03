
# DCore: What is it

The 'DCore' lib has two purposes:

- Place to put scripts that the main applications I develop can depend on and share (a core lib of some sort).
- Neat collection of scripts that make the computer a better development platform that I install on everyone of my computers.
- Easy install cloud service to any cloud node I own.

# TODO

- Have an install.sh that justs sets everything up so that you can be on a new nix or windows system and just get started.
    - Make sure the scripts shortcut are install so that can be easier to setup other things in cron.
    - Steps missing:
        - First run: setting pythonpath so that import dcore works from everywhere
        - Have a script that setups all kind of links & dirs

- Have a way to setup service that are checked to work every minute, if not work send e-mail. (cron + on run, if not run restart).
    - */5 * * * * root python3 /home/.../dcore/apps/report_to_cloud/report_to_cloud.py 
    - https://pypi.python.org/pypi/python-daemon/ ? <-- does not support p3!

# Notes

- This is shared on github, so put all personal information elsewhere :P.
- Look into: https://pypi.python.org/pypi/appdirs to store data in the right place on different OSes.

# Structure

    ./             : library scripts; imported from application. This is a sort of 'core-lib'.
    ./shell_ext    : small utilities (all contained in a file) invokable from the command-line.
    ./system_setup : scripts that make system-wide changes to setup the productivity scripts.
    ./apps         : complete applications that can depend on any dcore infrastructure (except from _shell_ext).

## Rules

- No one depends on the scripts in 'shell_ext' or 'apps', they are leaf modules.

