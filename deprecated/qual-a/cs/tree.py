"""
Generic n-ary tree with some helper functions implemented.

Does not enforce order of nodes, NOT a search tree. See bst.py for search tree.

# Improvements

- Might be better to have a tree class that manages the node. Each node having a unique ID guaranteed
by the tree class would help for debugging and algorithms that copy nodes around.
"""

import os

class Node:

    def __init__(self, data = None):
        self.children = []
        self.data = data
        self.parent = None

    def __repr__(self):
        return self.__str__()

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


def idTree(root):
    nodeToId = {}
    #nodeToId[None] = -1

    idCount = 0
    for node in DFS(root):
        nodeToId[node] = idCount
        idCount += 1
    return nodeToId


def findNodeWithData(root, data):
    for iNode in DFS(root):
        if iNode.data == data:
            return iNode
    return None

def DFS(node):
    for child in node.children:
        yield from DFS(child)
    yield node

def printTree(root):

    nodeToId = idTree(root)
    for node in DFS(root):
        C = [str(nodeToId[x]) for x in node.children]
        C = ", ".join(C)
        print('Node[%i]: value: %s, parent: %s, children(s): %s.' % (nodeToId[node], node.data, nodeToId[node.parent], C))
        
