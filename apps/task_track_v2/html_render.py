"""
Render using http://d3js.org/.
Excellent tutorial here: http://alignedleft.com/tutorials/d3.
"""

import os

import options
import work_unit
import serialization_json  

def render(wd, htmlFilename):
	template = open(os.path.join(options.mainDir, 'template.html')).read()
	open(htmlFilename, 'w').write(template)

def unitTests():
	filename = os.path.join(options.utFolder, 'unit-tests-render_html.html')
	wd = serialization_json.createTestData()
	render(wd, filename)

if __name__ == '__main__':
	unitTests()
