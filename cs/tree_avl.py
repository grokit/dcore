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

    def rotate(self, node, isLeftNode):
        print('rotate', isLeftNode)
        heightLeft, heightRight = AVLTree.childrenHeights(node)

        if isLeftNode:
            if heightLeft > heightRight:
                self.rotateLeftOuter(node)
                return
            else:
                crot = node.right
                self.rotateLeftInner(node)
                self.rotateLeftOuter(crot)
                return
        else:
            if heightRight > heightLeft:
                self.rotateRightOuter(node)
                return
            else:
                crot = node.left
                self.rotateRightInner(node)
                self.rotateRightOuter(crot)
                return

    def rotateRightOuter(self, node):
        n1 = node.parent
        n2 = node
        b = n2.left

        n2.parent = None
        n2.left = n1

        n1.right = b
        n1.parent = n2

        if b is not None:
            b.parent = n1

        self.root = n2
        
    def rotateLeftOuter(self, node):
        n1 = node.parent
        n2 = node
        b = n2.right

        n2.parent = None
        n2.right = n1

        n1.left = b
        n1.parent = n2

        if b is not None:
            b.parent = n1

        self.root = n2

    def rotateLeftInner(self, node):
        n1 = node.parent
        n2 = node
        n3 = node.right
        b1 = n3.left
        b2 = n3.right 

        n1.left = n3

        n3.parent = n1
        n3.right = b2
        n3.left = n2

        n2.parent = n3 
        n2.right = b1

        if b1 is not None:
            b1.parent = n2

    def rotateRightInner(self, node):
        n1 = node.parent
        n2 = node
        n3 = node.left
        b1 = n3.right
        b2 = n3.left 

        n1.right = n3

        n3.parent = n1
        n3.left = b2
        n3.right = n2

        n2.parent = n3 
        n2.left = b1

        if b1 is not None:
            b1.parent = n2

    def insert(self, data):
        node = Node(self.nextId, data)
        self.nextId += 1

        if self.root == None:
            self.root = node
        else:
            self.placeNode(node)

        # AVL re-balancing. 
        if True:
            heightLeft, heightRight = AVLTree.childrenHeights(self.root)
            if heightLeft - heightRight >= 2:
                self.rotate(self.root.left, True)
            if heightRight - heightLeft >= 2:
                self.rotate(self.root.right, False)

        # Reset all heights
        for node in inorderTraversal(self.root):
            node.height = 0

        for node in inorderTraversal(self.root):
            if node.left is None and node.right is None:
                updateHeightFromLeaf(node)

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
        return "%s (id: %s, h: %s)" % (self.data, self.id, height)
        #return "%s (h: %s)" % (self.data, height)

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
    #nodes = [10,9,8,7]
    #nodes = [7,8,9,10]
    #nodes = [20, 9, 8, 15, 16, 10]
    #nodes = [20, 9, 8, 15, 16, 10, 25, 19, 30]
    nodes = [76, 1,2,3,4, 22, 45, 29, 44, 50, 1000,13,99,100,98]

    for i, v in enumerate(nodes):
        tree.insert(v)
        dot.graphToPng(treeIterateAdaptor(tree), name = 'graph_%.2i' % i)

    dot.graphToPng(treeIterateAdaptor(tree), name = 'graph_final')
    nodesOut = [n for n in inorderTraversal(tree.root)]

    nodes.sort()
    print(nodesOut, nodes)
    pairs = [(a.data, b) for a, b in zip(nodesOut, nodes)]
    for a, b in pairs:
        print(a,b)
        assert a == b

if __name__ == '__main__':
    test()

