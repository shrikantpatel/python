class Solution:

    def numIslands(self, grid: list[list[str]]) -> int:
        
        totalRow = len(grid)
        totalCol = len(grid[0])
        noOfIsland = 0

        for row in range(0, totalRow) :

            for col in range(0, totalCol) :
                if grid[row][col] == '1' :
                    noOfIsland += 1
                    self.markAllAdjacentLand(row, col, grid)

        return noOfIsland


    def markAllAdjacentLand(self, row, col, grid:list[list[str]]) :
        totalRow = len(grid)
        totalCol = len(grid[0])

        if row == totalRow : return
        if col == totalCol : return
        if col == -1 : return
        if row == -1 : return

        if (grid[row][col] == '1') :
            grid[row][col] = 'X'
            self.markAllAdjacentLand(row+1, col, grid)
            self.markAllAdjacentLand(row, col+1, grid)
            self.markAllAdjacentLand(row-1, col, grid)
            self.markAllAdjacentLand(row, col-1, grid)
        else :
            return