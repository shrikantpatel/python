# https://leetcode.com/problems/sort-colors/
class Solution:
    
    def sortColors(self, nums: list[int]) -> None:

        # solving it using heap short
        def sort(begin: int, end :int) -> None:

            if (begin < end) :
                partitionIndex = partition(begin, end)
                sort(0, partitionIndex - 1)
                sort(partitionIndex + 1, end)
            return
        
        def partition(begin: int, end: int) -> int:

            pivot = nums[end]

            #pointer to value higher than pivot
            pointerToHigherVal = begin

            for counter in range(begin, end) :

                # number < pivot, swap the highest to lowest
                if nums[counter] < pivot:

                    #swap higher val and lower val
                    temp = nums[counter]
                    nums[counter] = nums[pointerToHigherVal]
                    nums[pointerToHigherVal] = temp
                    pointerToHigherVal += 1

            # swap the higher and pivot
            nums[end] = nums[pointerToHigherVal] 
            nums[pointerToHigherVal] = pivot

            return pointerToHigherVal
        
        sort(0, len(nums)-1)
        return

if __name__ == "__main__" :
    t1 = Solution()
    t1.sortColors([2,0,2,1,1,0])
    t1.sortColors([2,0,1])
    #t1.sortColors([2,2,1,2,1,1,1,0,0,2,1,0,2,1,2,2,1,1,1,1,1,0,2,0,2,0,2,2,1,0,2,1,0,2,1,2,0,0,0,0,2,1,1,2,0,1,2,2,0,0,2,2,0,1,0,1,0,0,1,1,1,0,0,2,2,2,1,0,0,2,1,0,1,0,2,2,1,2,1,1,2,1,1,0,0,2,1,0,0])