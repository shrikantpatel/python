class Solution:
    """
    Binary Search implementation for LeetCode problem 704.
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    """

    def search(self, nums: list[int], target: int) -> int:
        """
        Search for target in a sorted array using binary search.
        
        Args:
            nums: Sorted array of integers in ascending order
            target: The integer to search for
            
        Returns:
            Index of target if found, -1 otherwise
        """

        low = 0
        high = len(nums) - 1

        while low <= high:
            
            mid = low + (high - low) // 2

            # if the mid matches the target return it
            if nums[mid] == target:
                return mid
            # mid is greater than target, search left half
            if nums[mid] > target:
                high = mid - 1
            # mid is less than target, search right half
            if nums[mid] < target:
                low = mid + 1

        return -1

if __name__ == "__main__":
    s = Solution()
    
    # LeetCode examples
    assert s.search([-1, 0, 3, 5, 9, 12], 9) == 4, "example: target present"
    assert s.search([-1, 0, 3, 5, 9, 12], 2) == -1, "example: target absent"
    
    # Edge cases
    assert s.search([], 1) == -1, "empty list"
    assert s.search([1], 1) == 0, "single element found"
    assert s.search([1], 2) == -1, "single element not found"
    assert s.search([1, 2], 1) == 0, "two elements, first found"
    assert s.search([1, 2], 2) == 1, "two elements, second found"
    assert s.search([1, 2], 3) == -1, "two elements, not found"
    
    # Boundary tests
    assert s.search([1, 2, 3, 4, 5], 1) == 0, "target at beginning"
    assert s.search([1, 2, 3, 4, 5], 5) == 4, "target at end"
    assert s.search([1, 2, 3, 4, 5], 3) == 2, "target in middle"
    
    # Larger array
    assert s.search(list(range(0, 100, 2)), 50) == 25, "large array test"
    assert s.search(list(range(0, 100, 2)), 51) == -1, "large array, not found"
    
    print("All tests passed! ✅")
    
    # Performance demo (optional)
    import time
    large_array = list(range(1000000))
    start = time.time()
    result = s.search(large_array, 999999)
    end = time.time()
    print(f"Found {result} in {end-start:.6f} seconds for 1M elements")