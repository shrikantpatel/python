# look at git versino 1 -- non memory otimized version - beat 25 % of submission on memory
# look at git version 2 and comment for more details -- little better on memory otimized version - beat 55 % of submissions on memory
# look at git version 3 and comment for more details -- more memory otimized version - beat 81 % of submissions on memory
class Solution:

    def permute(self, nums: list[int]) -> list[list[int]]:
        
        completeList = []
        currentPermutation = []

        self.getPermutation(nums, currentPermutation, completeList)
        
        return completeList
    
    def getPermutation(self, nums: list[int], currentPermutation: list[int], completeList: list[list[int]]):
    

        if len(currentPermutation) == len(nums) :
            completeList.append(currentPermutation[:])
            return
    
        for i in nums :
            
            # remove the need previously used variable unusedNumber to track the number already visited.
            # we directly check that if curent number exists in the currentPermutation
            if i not in currentPermutation :            
                
                currentPermutation.append(i)
                self.getPermutation(nums, currentPermutation, completeList)
                currentPermutation.pop()
        
if __name__ == "__main__" :
    t1 = Solution()
    t1.permute([1, 2, 3, 4])