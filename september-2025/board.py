import numpy as np

class Board:
    """
    <board> is a 2D list of numbers on the grid
    <hooks> is a list of length 8 specifying the direction of each hook
    """
    def __init__(self, board: list[list[int]] = [[]], hooks: list = []):
        if board == [[]]:
            board = [
                [0,0,0,0,5,0,0,0,0],
                [0,0,0,4,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,8,0,0,0],
                [0,0,0,0,9,0,0,0,0]
            ]
        self.visited = [[False]*9 for i in range(9)]
        self.board = board
        self.hooks = hooks
        self.counts = [0]*9

        cornerPositions = []
        row, col = 4, 4
        center = (4,4)
        for i in range(len(self.hooks)):
            if self.hooks[i] == 1:
                row = center[0] - ((i/2)+1)
                col = center[1] - ((i/2)+1)
                center = (center[0]-0.5, center[1]-0.5)
            elif self.hooks[i] == 2:
                row = center[0] - ((i/2)+1)
                col = center[1] + ((i/2)+1)
                center = (center[0]-0.5, center[1]+0.5)
            elif self.hooks[i] == 3:
                row = center[0] + ((i/2)+1)
                col = center[1] + ((i/2)+1)
                center = (center[0]+0.5, center[1]+0.5)
            elif self.hooks[i] == 4:
                row = center[0] + ((i/2)+1)
                col = center[1] - ((i/2)+1)
                center = (center[0]+0.5, center[1]-0.5)
            
            if row < 0 or col < 0 or row >= len(self.board) or col >= len(self.board):
                raise Exception("Invalid hooks")
            
            cornerPositions.append((int(row), int(col)))

        self.corners = cornerPositions
                
    def showCorners(self):
        cornerBoard = [[0]*9 for i in range(9)]
        cornerBoard[4][4] = 1
        for i, corner in enumerate(self.corners):
            cornerBoard[corner[0]][corner[1]] = i+2
        for row in cornerBoard:
            print(row)
    
    def checkHooks(self) -> bool:
        """
        Check that ordering of hooks is valid and fills the grid
        The correct amount of numbers are in each hook
        --> Return or log the issue somehow if it's invalid
        """
        for i, corner in enumerate(self.corners):
            counter = {}
            directions = [(1,1), (1,-1), (-1,-1), (-1,1)]
            direction = directions[self.hooks[i]-1]
            row, col = corner[0], corner[1]
            value = 0
            for j in range(i+2):
                rowIndex, colIndex = row+direction[0]*j, col+direction[1]*j
                rowVal, colVal = self.board[rowIndex][col], self.board[row][colIndex]
                if rowVal != 0:
                    value = rowVal
                    counter[rowVal] = 1 + counter.get(rowVal, 0)
                if colVal != 0 and j != 0:
                    counter[colVal] = 1 + counter.get(colVal, 0)
            
            print(counter, value)
            if len(counter) > 1 or counter.get(value, -1) != value:
                return False
                
        return True
    
    def _bfs(self, row=4, col=4) -> int:
        if (row < 0 or col < 0 or row >= len(self.board) or col >= len(self.board) or 
            self.board[row][col] == 0 or self.visited[row][col] is True
        ):
            return 0
        
        self.counts[self.board[row][col]-1] += 1
        self.visited[row][col] = True

        up = self._bfs(row-1, col)
        down = self._bfs(row+1, col)
        left = self._bfs(row, col-1)
        right = self._bfs(row, col+1)

        return up+down+left+right+1

    def checkAdjacent(self) -> bool:
        """
        Use bfs to make sure all numbers are connected
        """    
        return self._bfs() == 45
    
    def checkCounts(self) -> bool:
        """
        Checks that all numbers appear the right amount of times
        Requires that a _bfs call occurs beforehand to update self.counts
        """
        for i in range(len(self.counts)):
            if i+1 != self.counts[i]:
                return False
        return True
    
    def _checkNumber(self, value, direction: str, position: int) -> bool:
        """
        Checks a number on the side of the board

        Args:
            value: the value that needs to be seen first
            direction: the direction to start the search (up, down, left, or right)
            position: the index of the row or column 
        """
        index = 0 if direction == "down" or direction == "right" else len(self.board)-1

        boardVal = self.board[position][index] if (direction == "left" or direction == "right") else self.board[index][position]
        while boardVal == 0:
            if direction == "down" or direction == "right": index += 1
            else: index -= 1

            if index < 0 or index >= len(self.board): return False 

            boardVal = self.board[position][index] if direction == "left" or direction == "right" else self.board[index][position]
        return boardVal == value

    def checkSquares(self) -> bool:
        arr = np.array(self.board)
        # Extract 2x2 windows by overlapping slices
        top_left = arr[:-1, :-1]
        top_right = arr[:-1, 1:]
        bot_left = arr[1:, :-1]
        bot_right = arr[1:, 1:]

        # Each 2x2 block has a zero if min across its 4 elements is 0
        has_zero = (top_left == 0) | (top_right == 0) | (bot_left == 0) | (bot_right == 0)
        return np.all(has_zero)

    def checkNumbers(self):
        """
        Use bfs to make sure all numbers are connected
        Check that the right amount of numbers are in the grid
        Check the outer values line up
        No 2x2 fillings
        """
        isAdjacent = self.checkAdjacent()
        correctCounts = self.checkCounts()

        numbers = [
            self.board[4][4] == 1,
            self._checkNumber(2, "left", 5),
            self._checkNumber(3, "up", 2),
            self.board[1][3] == 4,
            self.board[0][4] == 5,
            self._checkNumber(6,"right",3),
            self._checkNumber(7,"down",6),
            self.board[7][5] == 8,
            self.board[8][4] == 9
        ]
        
        return {
            "isValid": isAdjacent and correctCounts and numbers == [True]*9,
            "isAdjacent": isAdjacent,
            "correctCounts": correctCounts,
            "counts": self.counts,
            "validNumbers": numbers
        }

    def checkPentominoes(self) -> bool:
        """
        Use the outer numbers to search for pentominoes
        Make sure each pentomino adds up to a multiple of 5
        9 distince pentominoes
        """

        # Check I in the first row from left

        # Check U in the first row from right

        # Check X in the 4th row from left

        # Check N in 6th row from right

        # Check Z in 9th row from left

        # Check V in 9th row from right