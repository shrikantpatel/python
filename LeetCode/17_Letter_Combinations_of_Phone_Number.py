class Solution:
    def letterCombinations(self, digits: str) -> list[str]:

        self.ans = []
        previousString = ''
        currentIndex = 0

        if len(digits) != 0 :
            self.buildPermutation(previousString, currentIndex, digits)

        return self.ans
    
    def buildPermutation(self, previousString, currentIndex, digits) :
         
         currentChar = digits[currentIndex]
         charArray = self.getCharsForDigit(currentChar)
         
         for c in charArray : 

            if currentIndex == len(digits) -1 :
                temp = previousString + c
                self.ans = self.ans + [temp]
            else :
                self.buildPermutation(previousString + c, currentIndex+1, digits)

    def getCharsForDigit(self, character) :

        match character :
            case '2':
                return ['a', 'b', 'c']
            case '3':
                return ['d', 'e', 'f']
            case '4':
                return ['g', 'h', 'i']
            case '5':
                return ['j', 'k', 'l']
            case '6':
                return ['m', 'n', 'o']
            case '7':
                return ['p', 'q', 'r', 's']
            case '8':
                return ['t', 'u', 'v']
            case '9':
                return ['w', 'x', 'y', 'z']
            

def test_sum():
    assert sum([1, 2, 3]) == 6, "Should be 6"

if __name__ == "__main__":
    test_sum()
    print("Everything passed")