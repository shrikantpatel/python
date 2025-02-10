class Solution :

    def generateParenthesis(self, maxPairs: int) -> list[str]:
        anslist = []
        startParenthesis = 0
        endParenthesis = 0
        self.recursivelyGenerateParenthesis(startParenthesis, endParenthesis, maxPairs, "", anslist)
        return anslist

    def recursivelyGenerateParenthesis(self, startParenthesis :int, endParenthesis: int, maxPairs: int, ans: str, anslist: list[str]):
                
        if startParenthesis < maxPairs :
            self.recursivelyGenerateParenthesis(startParenthesis+1, endParenthesis, maxPairs, ans + "(", anslist)

        if endParenthesis < startParenthesis :
            self.recursivelyGenerateParenthesis(startParenthesis, endParenthesis+1, maxPairs, ans + ")", anslist)

        if (startParenthesis == endParenthesis and endParenthesis == maxPairs) :
            anslist = anslist.append(ans)
            return


if __name__ == "__main__" :
    t1 = Solution()
    # assert t1.generateParenthesis([1, 2, 3, 4, 4], 8) == True, "Should be true"
    # assert t1.generateParenthesis([1, 2, 3, 4, 5], 10) == False, "Should be false"
    # assert t1.generateParenthesis([1, 2, 3, 4, 5], 0) == False, "Should be false"
    # assert t1.generateParenthesis([1, 2, 3, 4, 5], 9) == True, "Should be True"
    # assert t1.generateParenthesis([5, 2, 3, 4, 1], 9) == True, "Should be True"