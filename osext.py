
import subprocess
import tempfile
import os

class OsExtException(BaseException):
    pass

def execute(cmd):
    """
    Execute a OS command, throw an exception if the return code isn't 0.
    
    Returns everything that was put on stdout and stderr.
    """
    
    fh = tempfile.NamedTemporaryFile(delete=False)
    return_code = subprocess.check_call(cmd, stderr=fh, stdout=fh, shell=False)
    filename = fh.name
    fh.close()
    
    fh = open(filename, 'r')
    std_all = fh.read()
    fh.close()
    
    tryno = 0
    done = False
    while(not done):
        try:
            os.unlink(filename)
            done = True
        except Exception as e:
            tryno += 1
            print(e)
            if tryno > 100000:
                raise e
        
    assert(not os.path.exists(filename))
    
    return std_all

def test_module():
    execute('dir')
    
    isFail = False
    try:
        execute('invalid_for_sure command')
    except OsExtException as e:
        isFail = True
    assert( isFail )
    
if __name__ == '__main__':
    test_module()
