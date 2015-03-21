
import os 

def graphToPng(graphIterator, name='graph'):
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

        for c in node.children:
            if c is not None:
                L.append('%s -> %s;' % (node.id, c.id))

    L.append("}")
    s = "\n".join(L)
    name = os.path.expanduser('~/' + name)
    fh = open('%s.dot' % name, 'w')
    fh.write(s)
    fh.close()

    cmd = gb + ' -Tpng %s.dot -O' % name
    print(cmd)
    os.system(cmd)
