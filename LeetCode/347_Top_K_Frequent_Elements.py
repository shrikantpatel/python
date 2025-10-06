#https://leetcode.com/problems/top-k-frequent-elements/
from collections import Counter
import heapq

class Solution:
    
    def topKFrequent(self, nums: list[int], k: int) -> list[int]: 
        # O(1) time 
        if k == len(nums):
            return nums
        
        # 1. build hash map : character and how often it appears
        # O(N) time
        count = Counter(nums)   
        # 2-3. build heap of top k frequent elements and
        # convert it into an output array
        # O(N log k) time
        return heapq.nlargest(k, count.keys(), key=count.get) 
    

if __name__ == "__main__" :
    t1 = Solution()
    assert t1.topKFrequent([1,1,1,2,2,3], 2) == [1, 2], 'Should be true'
    assert t1.topKFrequent([1], 1) == [1], 'Should be true'

