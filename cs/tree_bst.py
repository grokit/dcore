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
            self.__placeNode(node)

    def __placeNode(self, node, cursor = None):
        if cursor is None:
            cursor = self.root

        if node.data >= cursor.data:
            if cursor.right is None:
                cursor.right = node
                node.parent = cursor
                updateHeightFromLeaf(node)
            else:
                self.__placeNode(node, cursor.right)
        else:
            if cursor.left is None:
                cursor.left = node
                node.parent = cursor
                updateHeightFromLeaf(node)
            else:
                self.__placeNode(node, cursor.left)

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
        return "%s (id: %s, height: %s)" % (self.data, self.id, height)

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

if __name__ == '__main__':
    test()

