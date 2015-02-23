"""
Rename files / folders with nice, commonly used patterns.

# TODO

- Prepend ISO date: 2014-01-01_<filename>
"""

import re
import os

_meta_shell_command = 'rename_files'

def isNum(s):
	try:
		int(s)
	except:
		return False
	return True

if __name__ == '__main__':
	files = os.listdir('.')
	files = [f for f in files if os.path.isfile(f)]

	for f in files:
		to = re.sub('[ ()]', '_', f)
		
		L = []
		for i in range(0, len(to)):
			if i != len(to)-1:
				if isNum(to[i]) and not isNum(to[i+1]):
					if i == 0 or not isNum(to[i-1]):
						L.append('0')
			L.append(to[i])
		to = "".join(L)
		print("%s -> %s" % (f, to))
		os.rename(f, to)
			
		
