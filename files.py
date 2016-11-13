
import os
import shutil
import time

def getUniqueDateFile(base, ext = '.txt'):
    filename = base + time.strftime("%Y-%m-%d_%H-%M-%S") + ext
    
    # If file already exist, pick a different filename.
    # I would prefer if that used a predictable, increasing sequence instead of random.
    while os.path.isfile(filename):
        random.seed(time.time())
        randomArr = 'abcdefghijklmnpoqrstuvwxyz'
        randomChar = randomArr[random.randint(0, len(randomArr)-1)]
        filename = filename.replace('.', '_%s.' % randomChar )
    
    return filename
    
"""
def rm_then_mk_folder(folder):
  
  if os.path.isdir(folder):
    shutil.rmtree(folder)
  
  if not os.path.isdir(folder):
    os.mkdir(folder)
"""
