import re
import os

def isNum(s):
	try:
		int(s)
	except:
		return False
	return True

files = os.listdir('.')
files = [f for f in files if os.path.isfile(f)]

for f in files:
	print(f)
	#to = f.replace(' ', '_')
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
		
	
