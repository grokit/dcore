
import os
import getpass 

import globals.log as log

def createAdminPasswordDoesNotExpire(username, password = None):
    # make sure you are administrator
    
    if password is None:
        password = getpass.getpass("%s's sassword: " % username)
    
    cmds = """
    net user /add {0} {1}
    net localgroup administrators {0} /add
    net user {0} /expires:never
    """.format(username, password)
    
    cmds = cmds.splitlines()
    
    for cmd in cmds:
        print(cmd)
        os.system(cmd)
    
    os.system('net users')

if __name__ == '__main__':
    #createAdminPasswordDoesNotExpire('cron')
    
    log.debug("Begin cron.")
    
    log.debug("End cron.")
