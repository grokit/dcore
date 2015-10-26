"""
Render using http://d3js.org/.
Excellent tutorial here: http://alignedleft.com/tutorials/d3.
"""

import os
import json
import copy
import time
import re

import options
import work_unit
import serialization_json  

def render(wd, htmlFilename):
	template = open(os.path.join(options.mainDir, 'template.html')).read()
	open(htmlFilename, 'w').write(template)

	workUnits = serialization_json.fromFile(options.dbFile)

	def dateToUnixTime(w):
		ww = copy.deepcopy(w)
		dd = time.mktime(ww.date.timetuple())
		ww.date = dd
		return ww

	workUnits = list(map( dateToUnixTime, workUnits))

	filenameOut = 'data.js'
	ser = json.dumps(workUnits, cls=serialization_json.Encoder, indent=4)
	# Need to dump as javascript object...
	lines = ser.split('\n')
	out = ['var data =']
	for l in lines:
		l = re.sub(r'"(\w+)":', r'\1:', l)
		l = re.sub(r'comment.*?".*?"', r'comment:"anon"', l)
		out.append(l)

	open(filenameOut, 'w').write("\n".join(out))

def unitTests():
	filename = os.path.join(options.utFolder, 'unit-tests-render_html.html')
	wd = serialization_json.createTestData()
	render(wd, filename)

if __name__ == '__main__':
	unitTests()
