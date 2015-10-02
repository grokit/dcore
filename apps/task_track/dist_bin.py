
import sys
from cx_Freeze import setup, Executable

sys.argv.append('build_exe')

setup(
    name="task_track",
    version="1.0",
    description="bin from pxfreeze",
    executables=[Executable("enter_task.pye")])
