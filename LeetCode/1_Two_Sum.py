class Solution:
    """
    LeetCode Problem 1: Two Sum
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    def twoSum(self, nums: list[int], target: int) -> list[int]:
        """
        Find two numbers in the array that add up to target.
        
        Args:
            nums: List of integers
            target: Target sum
            
        Returns:
            List containing indices of the two numbers that add up to target
        """
        complement = {} 
        for index, num in enumerate(nums):
            if num in complement:
                return [complement[num], index]
            complement[target - num] = index
        return []  # Should never reach here per problem constraints


if __name__ == "__main__":
    s = Solution()

    def _assert_pairs_equal(a: list[int], b: list[int]) -> None:
        """Helper function to compare pairs regardless of order."""
        assert sorted(a) == sorted(b), f"Expected {b}, got {a}"

    # LeetCode examples
    _assert_pairs_equal(s.twoSum([2, 7, 11, 15], 9), [0, 1])
    _assert_pairs_equal(s.twoSum([3, 2, 4], 6), [1, 2])
    _assert_pairs_equal(s.twoSum([3, 3], 6), [0, 1])
    
    # Additional test cases
    _assert_pairs_equal(s.twoSum([1, 2, 3, 4], 7), [2, 3])  # Sum at end
    _assert_pairs_equal(s.twoSum([5, 1], 6), [0, 1])        # Two elements
    _assert_pairs_equal(s.twoSum([0, 4, 3, 0], 0), [0, 3])  # Zero values
    _assert_pairs_equal(s.twoSum([-1, -2, -3, -4, -5], -8), [2, 4])  # Negatives

    print("All tests passed! ✅")
    
    # Performance demonstration
    import time
    large_nums = list(range(10000)) + [99999]  # Last two sum to target
    large_nums[5000] = 50000  # Make index 5000 and 9999 sum to 149999
    start = time.time()
    result = s.twoSum(large_nums, 149999)
    end = time.time()
    print(f"Found indices {result} in {end-start:.6f} seconds for 10K elements")