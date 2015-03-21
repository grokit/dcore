
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
        L.append('%s [label="%s"];' % (node.id, str(node.id) + "_" +str(node.data)))
        if node.parent is not None:
            L.append('%s -> %s [color=lawngreen, constraint=false]; // (c->parent)' % (nodeToId[node], nodeToId[node.parent]))
        for c in node.children:
            print(c)
            if c is not None:
                L.append('%s -> %s;' % (node.id, c.id))

    L.append("}")
    s = "\n".join(L)
    #print(s)
    fh = open('%s.dot' % name, 'w')
    fh.write(s)
    fh.close()

    cmd = gb + ' -Tpng %s.dot -O' % name
    print(cmd)
    os.system(cmd)
