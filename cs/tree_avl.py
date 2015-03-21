"""
AVL tree.

# TODOs

- Duplicates?

# References

- MIT intro to algo: https://www.youtube.com/watch?v=FNeL18KsWPc
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
            else:
                self.__placeNode(node, cursor.right)
        else:
            if cursor.left is None:
                cursor.left = node
            else:
                self.__placeNode(node, cursor.left)

class Node:
    def __init__(self, id, data):
        self.id = id
        self.data = data

        # Can AVL tree be non-binary?
        self.left = None
        self.right = None

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
        node.parent = None
        node.children = [node.left, node.right]
        yield node

def test():
    tree = AVLTree()
    nodes = [1, 6, 10,39,22,45, 29,44,50,125012,1000,13,99,100,98]
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

