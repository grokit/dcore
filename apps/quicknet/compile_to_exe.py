# need to run 'python compile_to_exe.py build' from cmd line

from cx_Freeze import setup, Executable

# icon="logo.ico", 
executables = [
        Executable("quicknet.py", appendScriptToExe=True, appendScriptToLibrary=False)
]

buildOptions = dict(
        create_shared_zip = False)

setup(
        name = "out",
        version = "0.1",
        description = "cx_Freeze",
        options = dict(build_exe = buildOptions),
        executables = executables)