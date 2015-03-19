"""
AVL tree.

# TODOs

- Duplicates?

# References

- MIT intro to algo: https://www.youtube.com/watch?v=FNeL18KsWPc
"""

import collections

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

    def __placeNode(self, node):
        pass

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

def BFS(node):
    S = collections.deque()
    S.append(node)

    while len(S) > 0:
        n = S.popleft()
        yield n
        if n.left is not None:
            S.append(n.left)
        if n.right is not None:
            S.append(n.right)

def test():
    tree = AVLTree()
    nodes = [10,39,22,40,29,44,12,1000,13,99,100,98]
    insertAll(tree, nodes)

    nodesOut = []
    for node in BFS(tree.root):
        nodesOut.append(node)

    nodes.sort()
    print(nodesOut, nodes)
    pairs = [(a,b) for a in nodesOut for b in nodes]
    for a,b in pairs:
        print(a,b)
        assert a == b

if __name__ == '__main__':
    test()

