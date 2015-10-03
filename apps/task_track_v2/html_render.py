"""
http://d3js.org/ ??
"""

import work_unit

def render(wd, htmlFilename):
	template = open('template.html').read()
	open(htmlFilename, 'w').write(template)

def unitTests():
	filename = 'unit-tests-%s.html' % __file__
	wd = work_unit.createTestData()
	render(wd, filename)

if __name__ == '__main__':
	unitTests()


