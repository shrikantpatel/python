class Solution:
    def searchRange(self, nums: list[int], target: int) -> list[int]:

        test = [-1, -1]

        def recursiveSearch(start : int, end : int, maxLength : int) -> list[int] :
            
            if (maxLength == 0) : 
                return
            if (target > nums[end]) : 
                return
            if (target < nums[start]) : 
                return
            
            if (start > end ) : return

            centerIndex = (start + end) // 2;

            # if taget is less than cenrtal element, search the left side of the list
            if (nums[centerIndex] > target) :
                return recursiveSearch(start, centerIndex-1, maxLength)

            # if taget is greater than cenrtal element, search the right side of the list
            if (nums[centerIndex] < target) :
                return recursiveSearch(centerIndex+1, end, maxLength)

            # we found the the target
            if (nums[centerIndex] == target) :
                
                # Go left of center to find any more occurence of the target 
                # this gives the starting index of this target
                startIndex = centerIndex
                i = centerIndex-1
                while i >=0 and nums[i] == target :
                    startIndex = i  
                    i -= 1

                # Go right of center to find any more occurence of the target 
                # this gives the ending index of this target
                endIndex = centerIndex
                i = centerIndex+1
                while i < maxLength and nums[i] == target :
                    endIndex = i
                    i += 1
                    
                return [startIndex, endIndex] 

        ans =  recursiveSearch(0, len(nums)-1, len(nums))
        
        # answer if null, we did find the target.
        if ans == None :
            ans = [-1, -1]
        return ans

    
        
if __name__ == "__main__" :
    t1 = Solution()
    assert t1.searchRange([5,7,7,8,8,10], 8) == [3,4], 'Should be true'
    assert t1.searchRange([5,7,7,8,8,10], 6) == [-1,-1], 'Should be true'
    assert t1.searchRange([], 0) == [-1,-1], 'Should be true'
    assert t1.searchRange([1], 1) == [0,0], 'Should be true'
    assert t1.searchRange([1,3], 1) == [0,0], 'Should be true'
    assert t1.searchRange([2,2], 3) == [-1, -1], 'Should be true'