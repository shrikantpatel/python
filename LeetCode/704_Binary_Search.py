class Solution:
    def search(self, nums: list[int], target: int) -> int:
        return 0


if __name__ == "__main__":
    s = Solution()
    # LeetCode examples + a few edge cases
    assert s.search([-1, 0, 3, 5, 9, 12], 9) == 4, "example: target present"
    assert s.search([-1, 0, 3, 5, 9, 12], 2) == -1, "example: target absent"
    assert s.search([], 1) == -1, "empty list"
    assert s.search([1], 1) == 0, "single element found"
    assert s.search([1, 2], 2) == 1, "two elements found"
    print("All tests passed")