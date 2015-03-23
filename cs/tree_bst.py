"""
"""

import collections
import random

import dot 

class NodeType:
    NoParent = 0
    LeftOfParent = 1
    RightOfParent = 2

    def getNodeType(node):
        if node.parent is None:
            return NodeType.NoParent

        if node.parent.left is not None and node.parent.left == node:
            return NodeType.LeftOfParent

        if node.parent.right is not None and node.parent.right == node:
            return NodeType.RightOfParent

        raise Exception("Invalid node: %s." % node)

class TreeBST:

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

def smallest(node):
    if node.left is None:
        return node
    else:
        return smallest(node.left)

def successor(node):

    nodeType = NodeType.getNodeType(node)

    if nodeType == NodeType.NoParent:
        if node.right is None:
            return None
        else:
            return smallest(node.right)

    if nodeType == NodeType.LeftOfParent:
        if node.right is None:
            return node.parent
        else:
            return smallest(node.right)

    if nodeType == NodeType.RightOfParent:
        if node.right is None:
            n = node.parent
            while True:
                nt = NodeType.getNodeType(n)
                if nt == NodeType.LeftOfParent:
                    return n.parent
                if nt == NodeType.NoParent:
                    return None
                n = n.parent
        else:
            return smallest(node.right)

    raise Exception()

def getTree():
    tree = TreeBST()
    values = [22, 45, 29, 44, 50, 125012,1000,13,99,100,98]
    insertAll(tree, values)
    return tree, values

def getTreeRandomNoDuplicate():
    tree = TreeBST()
    values = []
    H = set()

    while len(values) < 100:
        v = random.randint(0, 1000)
        if v not in H:
            values.append(v)
            H.add(v)

    insertAll(tree, values)

    return tree, values

def verifyTreeMatchesValues(tree, values):
    values = sorted(values)
    valuesOut = [n for n in inorderTraversal(tree.root)]
    print(valuesOut, values)
    pairs = [(a.data, b) for a, b in zip(valuesOut, values)]
    for a, b in pairs:
        print(a,b)
        assert a == b

def verifySuccessors(tree, values):

    values = sorted(values)

    # Verify the get, get successor and get predecessor code. (Assumes no duplicate)
    valuesOut = [n for n in inorderTraversal(tree.root)]
    for node, val in [(a, b) for a, b in zip(valuesOut, values)]:
        nodeFound = tree.getNodeByValue(val)
        print('@', nodeFound, val)
        assert nodeFound.data == val

        i = values.index(val)
        nodeNext = successor(nodeFound)
        if i == len(values) - 1:
            assert nodeNext is None
        else:
            assert nodeNext is not None
            assert nodeNext.data == values[i+1]

def test():
    for i in range(100):
        tree, values = getTreeRandomNoDuplicate()

        if False:
            dot.graphToPng(treeIterateAdaptor(tree))

        verifyTreeMatchesValues(tree, values)
        verifySuccessors(tree, values)

if __name__ == '__main__':
    test()

