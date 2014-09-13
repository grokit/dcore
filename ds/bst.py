
import random

class Node:

    def __init__(self, value):
        self.parent = None
        self.left = None
        self.right = None
        self.value = value 

class BST:
    "Binary Search Tree"

    def __init__(self):
        self.root = Node(50)

    def insert(self, node):
        c = self.root

        while True:
            if c.value == node.value:
                return
            elif node.value < c.value:
                if c.left is None:
                    c.left = node
                    return
                else:
                    c = c.left
            elif node.value > c.value:
                if c.right is None:
                    c.right = node
                    return
                else:
                    c = c.right
                
    def asInorderArray(self):
        S = [(self.root, 0)]
        A = []
        while len(S) != 0:
            (n, s) = S.pop()
            if n is None:
                continue
            
            if s == 0:
                S.append( (n, 1) )
                S.append( (n.left, 0) )
            else:
                A.append( n.value )
                S.append( (n.right, 0) )
        return A

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




    

