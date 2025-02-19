class Solution :

    def pair_Matcing_Sum(self, numList : list[int], sum : int) -> bool :

        complementSet = []

        for i in numList :
            complement = sum - i
            if i in complementSet :
                return True
            else :
                complementSet = complementSet + [complement]
            
        return False;



if __name__ == "__main__" : 
    t1 = Solution()
    assert t1.pair_Matcing_Sum([1, 2, 3, 4, 4], 8) == True, "Should be true"
    assert t1.pair_Matcing_Sum([1, 2, 3, 4, 5], 10) == False, "Should be false"
    assert t1.pair_Matcing_Sum([1, 2, 3, 4, 5], 0) == False, "Should be false"
    assert t1.pair_Matcing_Sum([1, 2, 3, 4, 5], 9) == True, "Should be True"
    assert t1.pair_Matcing_Sum([5, 2, 3, 4, 1], 9) == True, "Should be True"