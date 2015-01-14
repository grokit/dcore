import os
import re

files = [os.path.join(dp, f)
         for dp, dn, filenames in os.walk('.') for f in filenames]

mp3 = set()
for file in files:
    try:
        content = open(file).read()
        matches = re.findall(r'http[^" *]*\.mp3', content)
        for m in matches:
            mp3.add('wget "' + m + '"')
        print(matches)
    except:
        pass

open('out', 'w').write("\n".join(mp3))
