import math
#test

class Solution:

    def reverse(self, x : int) -> int:

        MAX_INT = 2 ** 31 - 1 # 2,147,483,647
        MIN_INT = -2 ** 31    #-2,147,483,648

        ans =0
        qoutient = x
        reminder = 0

        while (qoutient != 0) :
            reminder = qoutient % 10 if qoutient > 0 else qoutient % -10
            qoutient =math.trunc(qoutient / 10)
            ans = (ans * 10) + reminder
            if ans > MAX_INT or ans < MIN_INT :
                 return 0

        print(ans)
        return ans


if __name__ == "__main__" :
    t1 = Solution()
    assert t1.reverse(123) == 321, "Should be 321"
    assert t1.reverse(-123) == -321, "Should be -321"
    assert t1.reverse(120) == 21, "Should be 21"