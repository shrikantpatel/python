class Solution:

    def twoSum(self, nums: list[int], target: int) -> list[int]:



if __name__ == "__main__":
    s = Solution()

    def _assert_pairs_equal(a: List[int], b: List[int]) -> None:
        assert sorted(a) == sorted(b), f"{a} != {b}"

    # LeetCode examples
    _assert_pairs_equal(s.twoSum([2, 7, 11, 15], 9), [0, 1])
    _assert_pairs_equal(s.twoSum([3, 2, 4], 6), [1, 2])
    _assert_pairs_equal(s.twoSum([3, 3], 6), [0, 1])

    print("All tests passed")