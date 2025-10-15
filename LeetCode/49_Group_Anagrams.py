# https://leetcode.com/problems/group-anagrams/description/

class Solution:

    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:

        anagram_groups : dict[str, list[str]] = {} # type: ignore

        for str in strs :
            sorted_str = "".join(sorted(str))
            anagram_groups.setdefault(sorted_str, []).append(str)

        return list(anagram_groups.values())


if __name__ == "__main__":
    # simple test harness that compares groups ignoring order
    def _normalize(groups):
        return {tuple(sorted(g)) for g in groups}

    s = Solution()

    tests = [
        (["eat", "tea", "tan", "ate", "nat", "bat"],
         [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]),
        ([""], [[""]]),
        (["a"], [["a"]]),
    ]

    for inp, expected in tests:
        out = s.groupAnagrams(inp)
        assert _normalize(out) == _normalize(expected), f"Failed for {inp}: got {out}"
    print("All tests passed")