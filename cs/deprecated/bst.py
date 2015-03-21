"""
Binary Search Tree with 0-2 children per node.
"""

import random
import os 

random.seed(112345)

class Node:

    def __init__(self, value):
        self.parent = None
        self.left = None
        self.right = None
        self.value = value 

    def __str__(self):
        l = None
        if self.left is not None:
            l = self.left.value
        r = None
        if self.right is not None:
            r = self.right.value
        p = None
        if self.parent is not None:
            p = self.parent.value
        return "%s, left: %s, right: %s, parent: %s" % (self.value, l, r, p) 

class BST:
    "Binary Search Tree"

    def __init__(self):
        self.root = Node(50)

    def insert(self, node):
        c = self.root

        while True:
            if c.value == node.value:
                return False
            elif node.value < c.value:
                if c.left is None:
                    c.left = node
                    node.parent = c
                    return True
                else:
                    c = c.left
            elif node.value > c.value:
                if c.right is None:
                    c.right = node
                    node.parent = c
                    return True
                else:
                    c = c.right
                
    def getNodeFromValue(self, v):

        n = self.root

        while v != n.value:
            if v > n.value:
                n = n.right
            else:
                n = n.left

            if n is None:
                return None

        return n

    def asInorderArray(self):
        L = []
        fn = lambda x: L.append(x.value)

        self.traverseInorder(fn)
        return L

    def traverseInorder(self):
        """
        TODO: Replace fn by yield.
        """

        S = [(self.root, 0)]
        while len(S) != 0:
            (n, s) = S.pop()
            if n is None:
                continue
            
            if s == 0:
                S.append( (n, 1) )
                S.append( (n.left, 0) )
            else:
                yield n
                S.append( (n.right, 0) )

    @staticmethod
    def isLeftChild(n, parent):
        if parent.left is None:
            return None
        if parent.left == n: return True
        return False
    
    @staticmethod
    def leftmostChild(n):
        while n.left is not None:
            n = n.left
        return n

    def toGraph(self):
        #gb = r'"C:\Program Files (x86)\Graphviz 2.28\bin\dot.exe"'
        gb = 'dot'
        L = []
        L.append("digraph G{")
        L.append('graph [ordering="out"];')

        def gannotate(x):
            nullName = "null_%s" % x.value

            if x.left is not None:
                L.append("%s -> %s;" % (x.value, x.left.value))
            else:
                L.append("%s[shape=point];" % (nullName+'l'))
                L.append("%s -> %s;" % (x.value, nullName+'l'))

            if x.right is not None:
                L.append("%s -> %s;" % (x.value, x.right.value))
            else:
                L.append("%s[shape=point];" % (nullName+'r'))
                L.append("%s -> %s;" % (x.value, nullName+'r'))
        
        self.traverseInorder(gannotate) 
        L.append("}")
        s = "\n".join(L)
        print(s)
        fh = open('g.dot', 'w')
        fh.write(s)
        fh.close()

        cmd = gb + ' -Tpng g.dot -O'
        os.system(cmd)

def buildRandomBST(n = 10):

    bst = BST()

    for i in range(0, n):
        n = Node(random.randint(0, 100))
        bst.insert(n)

    return bst

if __name__ == '__main__':
    bst = buildRandomBST(50)
    bstA = bst.asInorderArray()
    print(bstA)


