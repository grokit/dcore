"""
Implementation of AVL tree.

# Notes

- Care about balancing left/right *height*, not left/right number of children.

# TODOs

- Duplicates?

# References

- MIT intro to algo: https://www.youtube.com/watch?v=FNeL18KsWPc
- http://en.wikipedia.org/wiki/AVL_tree
"""

import collections

import dot 

class AVLTree:

    def __init__(self):
        self.nextId = 1
        self.root = None

    def insert(self, data):
        node = Node(self.nextId, data)
        self.nextId += 1

        if self.root == None:
            self.root = node
        else:
            self.placeNode(node)

    def placeNode(self, node, cursor = None):
        if cursor is None:
            cursor = self.root

        if node.data >= cursor.data:
            if cursor.right is None:
                cursor.right = node
                node.parent = cursor
                updateHeightFromLeaf(node)
            else:
                self.placeNode(node, cursor.right)
        else:
            if cursor.left is None:
                cursor.left = node
                node.parent = cursor
                updateHeightFromLeaf(node)
            else:
                self.placeNode(node, cursor.left)

    def getNodeByValue(self, val):
        return self.getNodeByValueIterate(val, self.root)

    def getNodeByValueIterate(self, val, node):
        if node is None:
            return node

        if val == node.data:
            return node

        if val > node.data:
            return self.getNodeByValueIterate(val, node.right)
        else:
            return self.getNodeByValueIterate(val, node.left)

def updateHeightFromLeaf(node, h = 0):
    if node.height == None:
        node.height = h

    if node.height < h:
        node.height = h

    if node.parent is not None:
        updateHeightFromLeaf(node.parent, h+1)
    
class Node:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.left = None
        self.right = None
        self.height = None
        self.parent = None

    def __str__(self):
        #return "%s" % (self.data)
        height = self.height
        if height == None:
            height = 'None'
        #return "%s (id: %s, height: %s)" % (self.data, self.id, height)
        return "%s" % (self.data)

    def __repr__(self):
        return "%s" % self.data

def insertAll(tree, nodes):
    for node in nodes:
        tree.insert(node)

def inorderTraversal(node):
    if node.left is not None:
        yield from inorderTraversal(node.left)

    yield node

    if node.right is not None:
        yield from inorderTraversal(node.right)

def treeIterateAdaptor(tree):
    for node in inorderTraversal(tree.root):
        dotNode = Node(node.id, node.data)
        dotNode.parent = node.parent
        dotNode.children = [node.left, node.right]
        dotNode.height = node.height
        yield dotNode

def test():
    tree = AVLTree()
    nodes = [22, 45, 29, 44, 50, 125012,1000,13,99,100,98]
    insertAll(tree, nodes)

    nodesOut = [n for n in inorderTraversal(tree.root)]

    dot.graphToPng(treeIterateAdaptor(tree))

    nodes.sort()
    print(nodesOut, nodes)
    pairs = [(a.data, b) for a, b in zip(nodesOut, nodes)]
    for a, b in pairs:
        print(a,b)
        assert a == b

    # Verify the get, get successor and get predecessor code. (Assumes no duplicate)
    for node, val in  [(a, b) for a, b in zip(nodesOut, nodes)]:
        nodeFound = tree.getNodeByValue(val)
        #print('@', nodeFound, val)
        assert nodeFound.data == val

if __name__ == '__main__':
    test()

