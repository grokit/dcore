"""
Generic n-ary tree with some helper functions implemented.

# Improvements

Might be better to have a tree class that manages the node. Each node having a unique ID guaranteed
by the tree class would help for debugging and algorithms that copy nodes around.
"""

import os

class Node:

    def __init__(self, data = None):
        self.children = []
        self.data = data
        self.parent = None

    def __repr__(self):
        return this.__str__(self)

    def __str__(self):
        if self.parent == None: 
            pN = True 
        else: 
            pN = False
        return "data: %s, nChildren: %s, parent: %s" % (self.data, len(self.children), pN)

def upApply(node, fn, state):
    """
    Applies function for node and all parents.
    """

    while node.parent is not None:
        fn(node, state)
        node = node.parent
    fn(node, state)

def toGraph(root):
    gb = 'dot'
    L = []
    L.append("digraph G{")
    L.append('graph [ordering="out"];')

    nodeToId = idTree(root)
    for node in DFS(root):
        L.append('%s [label="%s"];' % (nodeToId[node], str(nodeToId[node]) + "_" +str(node.data)))
        if node.parent is not None:
            L.append('%s -> %s [color=lawngreen, constraint=false]; // (c->parent)' % (nodeToId[node], nodeToId[node.parent]))
        for c in node.children:
            L.append('%s -> %s;' % (nodeToId[node], nodeToId[c]))

    L.append("}")
    s = "\n".join(L)
    print(s)
    fh = open('g.dot', 'w')
    fh.write(s)
    fh.close()

    cmd = gb + ' -Tpng g.dot -O'
    os.system(cmd)

def idTree(root):
    nodeToId = {}
    #nodeToId[None] = -1

    idCount = 0
    for node in DFS(root):
        nodeToId[node] = idCount
        idCount += 1
    return nodeToId

def printTree(root):

    nodeToId = idTree(root)
    for node in DFS(root):
        C = [str(nodeToId[x]) for x in node.children]
        C = ", ".join(C)
        print('Node[%i]: value: %s, parent: %s, children(s): %s.' % (nodeToId[node], node.data, nodeToId[node.parent], C))

def findNodeWithData(root, data):
    for iNode in DFS(root):
        if iNode.data == data:
            return iNode
    return None

def DFS(node):
    for child in node.children:
        yield from DFS(child)
    yield node
