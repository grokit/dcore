"""
http://d3js.org/ ??
"""

import work_unit

import os

def scriptDir():
    return os.path.dirname(os.path.abspath(__file__))

def render(wd, htmlFilename):
	template = open(os.path.join(scriptDir(), 'template.html')).read()
	open(htmlFilename, 'w').write(template)

def unitTests():
	filename = 'unit-tests-%s.html' % __file__
	wd = work_unit.createTestData()
	render(wd, filename)

if __name__ == '__main__':
	unitTests()


