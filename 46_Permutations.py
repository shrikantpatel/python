class Solution:

    def permute(self, nums: list[int]) -> list[list[int]]:
        
        completeList = []
        unusedNumber = nums.copy()
        currentPermutation = []

        self.getPermutation(unusedNumber, currentPermutation, completeList)
        
        return completeList
    
    def getPermutation(self, unusedNumber: list[int], currentPermutation: list[int], completeList: list[list[int]]):
    

        if len(unusedNumber) ==0 :
            completeList.append(currentPermutation)
            return
    
        for i in unusedNumber :
            
            unusedNumber1 = unusedNumber.copy()
            currentPermutation1 = currentPermutation.copy()

            unusedNumber1.remove(i)
            currentPermutation1.append(i)
            self.getPermutation(unusedNumber1, currentPermutation1, completeList)
            
        
if __name__ == "__main__" :
    t1 = Solution()
    t1.permute([1, 2, 3])