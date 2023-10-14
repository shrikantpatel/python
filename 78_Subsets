#https://leetcode.com/problems/subsets/
class Solution:

    def subsets(self, nums: list[int]) -> list[list[int]]:
        
        completeList = []
        currentCombination = []

        # add the first blank list to complete list
        completeList.append(currentCombination)

        index = 0
        for num in nums :
            
            # identify the current length of list 
            previousEndIndex = len(completeList)

            #add the current number to complete\ final list.
            completeList.append([num])

            # append current number to all previous element in the list
            # 0th element is []
            # start from 1 to previous end index, and keep adding the current element to all the previous list
            # clone the list before appending (Note\reason for this: list is passed by reference vs value)
            for i in range(1, previousEndIndex) :
                currentCombination = completeList[i].copy()
                currentCombination.append(num)
                completeList.append(currentCombination)                       

        return completeList

if __name__ == "__main__" :
    t1 = Solution()
    t1.subsets([1, 2, 3, 4])