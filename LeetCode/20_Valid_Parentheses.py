class Solution:

    def isValid(self, s: str) -> bool:
        """Return True if parentheses in s are balanced."""
        pairs = { '}':'{', ']':'[', ')':'('}
        stack: list[str] = []

        for char in s:
            if char in pairs.values():
                stack.append(char)
            elif char in pairs.keys():
                if not stack or stack.pop() != pairs[char]:
                    return False
            else:
                # unexpected character — treat as invalid (optional)
                return False

        return not stack

        

if __name__ == "__main__":
    s = Solution()
    tests = [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([)]", False),
        ("{[]}", True),
        ("", True),
        ("[", False),
        ("](", False),
    ]
    for inp, expected in tests:
        assert s.isValid(inp) == expected, f"{inp}: expected {expected}, got {s.isValid(inp)}"
    print("All tests passed")