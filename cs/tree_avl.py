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

    def childrenHeights(node):
        heightLeft = 0
        if node.left is not None:
            heightLeft = node.left.height
        heightRight = 0
        if node.right is not None:
            heightRight = node.right.height

        return (heightLeft, heightRight)

    def rotate(self, node):
        print('rotate')
        heightLeft, heightRight = AVLTree.childrenHeights(node)

        if heightLeft > heightRight:
            return self.rotateLeft(node)

    def rotateLeft(self, node):
        print('rotate left')
        node.parent.left = node.right
        node.right = node.parent
        node.parent = None

    def insert(self, data):
        node = Node(self.nextId, data)
        self.nextId += 1

        if self.root == None:
            self.root = node
        else:
            self.placeNode(node)

        # AVL re-balancing.
        heightLeft, heightRight = AVLTree.childrenHeights(self.root)
        if abs(heightLeft - heightRight) >= 2:
            self.rotate(self.root.left)

    def placeNode(self, node, cursor = None):
        if cursor is None:
            cursor = self.root

        if node.data >= cursor.data:
            if cursor.right is None:
                cursor.right = node
                node.parent = cursor
                updateHeightFromLeaf(node)
            else:
                return self.placeNode(node, cursor.right)
        else:
            if cursor.left is None:
                cursor.left = node
                node.parent = cursor
                updateHeightFromLeaf(node)
            else:
                return self.placeNode(node, cursor.left)

def updateHeightFromLeaf(node, h = 0):

    if node.height == None or node.height < h:
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
        #return "%s (id: %s, h: %s)" % (self.data, self.id, height)
        return "%s (h: %s)" % (self.data, height)

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
    nodes = [76, 1,2,3,4, 22, 45, 29, 44, 50, 1000,13,99,100,98]
    insertAll(tree, nodes)

    nodesOut = [n for n in inorderTraversal(tree.root)]

    dot.graphToPng(treeIterateAdaptor(tree))

    nodes.sort()
    print(nodesOut, nodes)
    pairs = [(a.data, b) for a, b in zip(nodesOut, nodes)]
    for a, b in pairs:
        print(a,b)
        assert a == b

if __name__ == '__main__':
    test()

