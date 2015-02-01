# DCore: What is it

The 'DCore' lib has two purposes:

- Place to put scripts that the main applications I develop can depend on and share (a core lib of some sort).
- Neat collection of scripts that make the computer a better development platform that I install on everyone of my computers.

# Notes

- This is shared on github, so put all personal information elsewhere :P.
- Look into: https://pypi.python.org/pypi/appdirs to store data in the right place on different OSes.

# Structure

    ./             : library scripts; imported from application. This is a sort of 'core-lib'.
    ./shell_ext    : small utilities (all contained in a file) invokable from the command-line.
    ./system_setup : scripts that make system-wide changes to setup the productivity scripts.
    ./apps         : complete applications that can depend on any dcore infrastructure (except from _shell_ext).

## Rules

- No one depends on the scripts in 'shell_ext', they are leaf modules.

