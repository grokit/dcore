"""
http://d3js.org/ ??
"""

import work_unit

import os

import options

def render(wd, htmlFilename):
	template = open(os.path.join(options.mainDir, 'template.html')).read()
	open(htmlFilename, 'w').write(template)

def unitTests():
	filename = os.path.join(options.utFolder, 'unit-tests-%s.html' % __file__)
	wd = work_unit.createTestData()
	render(wd, filename)

if __name__ == '__main__':
	unitTests()


