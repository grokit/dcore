
import os 

def ensureDir(f):
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)

def graphToPng(graphIterator, isBinary = True, name='graph'):
	"""
	Assuming nodes:
	- id
	- value
	- children enumerable for children
	"""

	gb = 'dot'
	L = []
	L.append("digraph G{")
	L.append('graph [ordering="out"];')

	for node in graphIterator:
		# Unique id -> what to display in the node circle.
		L.append('%s [label="%s"];' % (node.id, str(node)))

		# Parent
		if node.parent is not None:
			L.append('%s -> %s [color=blue, constraint=false]; // (c->parent)' % (node.id, node.parent.id))

		if isBinary:
			nullName = 'null'
			c = node.children
			if c[0] == None: 
				uniqueNullId = "%s_%s_%s" % (nullName, node.id, 'l')
				L.append("%s[shape=point];" % (uniqueNullId)) 
				L.append("%s -> %s;" % (node.id, uniqueNullId)) 
			else: 
				L.append("%s -> %s;" % (node.id, c[0].id)) 

			if c[1] == None: 
				uniqueNullId = "%s_%s_%s" % (nullName, node.id, 'r')
				L.append("%s[shape=point];" % (uniqueNullId)) 
				L.append("%s -> %s;" % (node.id, uniqueNullId)) 
			else: 
				L.append("%s -> %s;" % (node.id, c[1].id)) 

		else:
			for c in node.children:
				if c is not None:
					L.append('%s -> %s;' % (node.id, c.id))
			

	L.append("}")
	s = "\n".join(L)
	ensureDir(os.path.expanduser('~/tmp/'))
	name = os.path.expanduser('~/tmp/' + name)
	fh = open('%s.dot' % name, 'w')
	fh.write(s)
	fh.close()

	cmd = gb + ' -Tpng %s.dot -O' % name
	print(cmd)
	os.system(cmd)
