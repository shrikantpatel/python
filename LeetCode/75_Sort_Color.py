# https://leetcode.com/problems/sort-colors/
class Solution:
        
    def sortColors(self, nums: list[int]) -> None:
        
        arrSize = len(nums)
        countOf1 = 0
        countOf2 = 0
        countOf3 = 0

        for counter in range(0, arrSize) :
            val = nums[counter]
            match val :
                case 0 :
                    countOf1 += 1
                case 1 :
                    countOf2 += 1
                case 2 :
                    countOf3 += 1

        for counter in range(0, countOf1) :
            nums[counter] = 0

        for counter in range(countOf1, countOf1+ countOf2) :
            nums[counter] = 1
        
        for counter in range(countOf1+countOf2, countOf1+countOf2+countOf3) :
            nums[counter] = 2

        return

if __name__ == "__main__" :
    t1 = Solution()
    #t1.sortColors([2,0,2,1,1,0])
    #t1.sortColors([2,0,1])
    t1.sortColors([2,2,1,2,1,1,1,0,0,2,1,0,2,1,2,2,1,1,1,1,1,0,2,0,2,0,2,2,1,0,2,1,0,2,1,2,0,0,0,0,2,1,1,2,0,1,2,2,0,0,2,2,0,1,0,1,0,0,1,1,1,0,0,2,2,2,1,0,0,2,1,0,1,0,2,2,1,2,1,1,2,1,1,0,0,2,1,0,0])