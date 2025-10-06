#https://leetcode.com/problems/find-peak-element/

class Solution:
    def findPeakElement(self, nums: list[int]) -> int:
        previousIndex = 0
        peakIndex = 0
        lenght = len(nums)

        for counter in range(1,lenght) :
            if nums[counter-1] < nums[counter]:
                peakIndex = counter

        print (peakIndex)
        return peakIndex
        
if __name__ == "__main__" :
    t1 = Solution()
    assert t1.findPeakElement([1,2,3,1]) == 2, 'Should be true'
    assert t1.findPeakElement([1,2,1,3,5,6,4]) == 5, 'Should be true'
    assert t1.findPeakElement([1]) == 0, 'Should be true'
    assert t1.findPeakElement([1,2]) == 1, 'Should be true'
    assert t1.findPeakElement([1,2,3]) == 2, 'Should be true'