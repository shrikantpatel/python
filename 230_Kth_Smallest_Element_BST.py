class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):


    def kthSmallest(self, root, k):
        """
        :type root: TreeNode
        :type k: int
        :rtype: int
        """
        self.incrementalArray = []
        self.traverse(root)
        return self.incrementalArray[k]
    
    def traverse(self, node):
        if node:
            self.traverse(node.left)
            self.k = self.incrementalArray + node.val
            self.traverse(node.right)