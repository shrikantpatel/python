#https://leetcode.com/problems/kth-largest-element-in-an-array/description/
import heapq

class Solution:
    '''
    The main idea of this solution is to use a min-heap with a maximum size of k. 
    By doing this, we ensure that the smallest of the k largest elements is always on the top of the heap.
    '''
    def findKthLargest(self, nums: list[int], k: int) -> int:

        # create the heap with Kth element
        heap = nums[:k]

        # create heap of Kth element (sort them with lowest at top of the heap and highest at the bottom of the heap)
        heapq.heapify(heap)
        
        # iterate from k to end of the list
        for num in nums[k:]:

            # if number is greater the lowest element (ie 0th index) then remove the lowest element and add this to the heap
            if num > heap[0]:
                heapq.heappop(heap)
                heapq.heappush(heap, num)
        
        return heap[0]
    
if __name__ == "__main__" :
    t1 = Solution()
    assert t1.findKthLargest([3,2,1,5,6,4], 2) == 5, 'Should be true'
    assert t1.findKthLargest([3,2,3,1,2,4,5,5,6], 4) == 4, 'Should be true'