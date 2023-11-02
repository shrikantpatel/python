#https://leetcode.com/problems/word-search/
class Solution:
    
    def exist(self, board: list[list[str]], word: str) -> bool:
       
        # set the variable to be use between all the funcctional
        totalRow = len(board)
        totalCol = len(board[0])
        totalCharInWord = len(word);
        # track the which index in search string i am on
        wordIndexBeingCompared = 0;


        def findWord(row: int, col: int, wordIndexBeingCompared: int) -> bool:
    
            # row or col are outbound (less 0 or greater than max value ) we are not find the search the string
            if row < 0 or row >= totalRow or col < 0 or col >= totalCol :
                return False

            currentChar = board[row][col];

            # if current value is X is already visited and we can skip it.
            # So only proceed if its not X and it matches the character in the search string that we interested in
            if currentChar != 'X' and currentChar == word[wordIndexBeingCompared] :

                # if index of character in search word == to length of search word we found the match
                if wordIndexBeingCompared == totalCharInWord :
                    return True
            
                # set he current character as X to indicate this element is already visited
                board[row][col] = 'X';

                # iterate this function to all adjacent col and row values
                if findWord(row, col-1, wordIndexBeingCompared+1) : 
                    return True;
                if findWord(row, col+1, wordIndexBeingCompared+1) : 
                    return True;
                if findWord(row-1, col, wordIndexBeingCompared+1) : 
                    return True;
                if findWord(row+1, col, wordIndexBeingCompared+1) : 
                    return True;
                # reseting current character back to original value so next iteration do see 'X' in that place
                board[row][col] = currentChar;

            return False;

        # for loops to iterate to over the each element in the array.
        for row in range(0, totalRow) :
            for col in range(0, totalCol) :
                matchFound = findWord(row, col, wordIndexBeingCompared)
                if matchFound == True :
                    return True;
    
        return False


if __name__ == '__main__' :
    t1 = Solution()
    assert t1.exist([['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], 'ABCCE') == True, 'Should be true'
    assert t1.exist([['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], 'ABCCS') == True, 'Should be true'
    assert t1.exist([['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], 'ABCCT') == False, 'Should be false'
    assert t1.exist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "SEE") == True, 'Should be true'
    assert t1.exist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], 'ABCB') == False, 'Should be false'
    assert t1.exist([["C","A","A"],["A","A","A"],["B","C","D"]], 'AAB') == True, 'Should be true'