import random as rd

class BingoUtilMixin(object):
    def generateBingoBoard(self, dim = 5):
        """
        Generates sequential bingo board
        """
        bb = []
        i = 1
        for _ in range(dim):
            bb += [[x for x in range(i, i + dim)]]
            i += dim
        return bb
    
    def buildMap(self, bingo):
        """
        Builds number to coords map
        """
        numToCoordsMap = {}
        dim = len(bingo)
        for x in range(dim):
            for y in range(dim):
                numToCoordsMap[bingo[x][y]] = (x,y)
        return numToCoordsMap
    
    def randomizeMatrix(self, board):
        """
        randomized generated bingo board
        """
        for _ in range(25):
            x1, y1 = rd.randint(0, 4), rd.randint(0, 4)
            x2, y2 = rd.randint(0, 4), rd.randint(0, 4)
            temp = board[x1][y1]
            board[x1][y1] = board[x2][y2]
            board[x2][y2] = temp
        return board