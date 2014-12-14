"""
Generic n-ary tree with some helper functions implemented.
"""

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

def printBranches(root):
    #print('root: ', root)
    for node in DFS(root):
        #print('DFS yielded node: %s' % node)
        if len(node.children) == 0:
            fn = lambda x, y: y.append(x)
            state = []
            upApply(node, fn, state)
            #print('L: %s' % len(state))
            L = []
            for s in state:
                L.append(str(s.data))
            print("Branch: " + ", ".join(L))

def printTree(root):
    nodeToId = {}
    nodeToId[None] = -1

    idCount = 0
    for node in DFS(root):
        nodeToId[node] = idCount
        idCount += 1

    for node in DFS(root):
        C = [str(nodeToId[x]) for x in node.children]
        C = ", ".join(C)
        print('Node[%i]: value: %s, parent: %s, children(s): %s.' % (nodeToId[node], node.data, nodeToId[node.parent], C))

def DFS(node):
    for child in node.children:
        yield from DFS(child)
    yield node
