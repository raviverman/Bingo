from BingoUtilMixin import BingoUtilMixin

class Bingo(BingoUtilMixin):
    def __init__(self, dim=5, bingoBoard=None):
        """
        Generates bingo board for given dimension (def 5)
        """
        self.dim = dim
        if bingoBoard is None:
            self.bingoBoard = self.randomizeMatrix(self.generateBingoBoard())
        else:
            self.bingoBoard = bingoBoard

        self.map = self.buildMap(self.bingoBoard)
    
    def mark(self, num):
        """
        Marks the bingo tile as marked by making the number negative
        """
        x,y = self.map[num]
        if self.bingoBoard[x][y] > 0:
            self.bingoBoard[x][y] *= -1

    def show(self):
        """
        Prints the bingo board"
        """
        for x in range(self.dim):
            for y in range(self.dim):
                print("{:>4}".format(self.bingoBoard[x][y]), end='')
            print("\n")
    
    def evaluateBoard(self):
        """
        Evaluate board to find matches
        """
        matches = 0
        rdiag = True
        ldiag = True
        for x in range(self.dim):
            hmatch = True
            vmatch = True
            for y in range(self.dim):
                if self.bingoBoard[x][y] > 0:
                    hmatch = False
                if self.bingoBoard[y][x] > 0:
                    vmatch = False
            if self.bingoBoard[x][self.dim - x -1] > 0:
                rdiag = False
            if self.bingoBoard[x][x] > 0:
                ldiag = False
            if hmatch:
                matches += 1
            if vmatch:
                matches += 1
        if rdiag:
            matches += 1
        if ldiag:
            matches += 1

        return matches

if __name__ == "__main__":
    bb = Bingo()
    bb.show()
    m = input("Enter data:").split()
    for x in m:
        bb.mark(int(x))
    cnt = bb.evaluateBoard()
    bb.show()
    print(f"Matches : {cnt}")