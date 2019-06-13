from enum import  Enum

class state(Enum):
    white = 1
    black = 2
    whiteKing = 3
    blackKing = 4
    empty = 0


class board():
    def __init__(self, firstColor, sq):
        '''[Board constructor]
        Arguments:
            firstColor {[state]} -- First field color.
            sq {[int]} -- Field size in visualization.
        '''

        self.board = []
        for i in range(0, 8):
            tmp = []
            for i in range(0,8):
                tmp.append([state.empty, state.black, [0, 0]])
            self.board.append(tmp)

        for i in range(0, 8):
            for j in range(0, 8):
                self.board[i][j][2] = [(i + 1) * sq, (j + 1) * sq]
        self.setFieldsColor(firstColor)


    def setFieldsColor(self, firstFieldColor):
        '''[Method set fields color, based on first color in board.]
        Arguments:
            firstFieldColor {[state]} -- [First field color]
        '''

        firstColor = state.black
        secondColor = state.white

        if firstFieldColor == state.white:
            firstColor = state.white
            secondColor = state.black
        
        cnt = 0
        for i in range(0, 8):
            for j in range(0, 8):
                if cnt % 2 == 0:
                    self.board[i][j][1] = firstColor
                else:
                    self.board[i][j][1] = secondColor
                cnt += 1
            cnt -= 1


    def setFieldCord(self, x, y, cord = []):
        self.board[x][y][2] = cord

    def setPawnColor(self, x, y, Color):
        self.board[x][y][0] = Color

    def getFieldColor(self, x, y):
        return self.board[x][y][1]

    def getFieldCord(self, x, y):
        return self.board[x][y][2]

    def getPawnColor(self, x, y):
        return self.board[x][y][0]

    def countPawns(self):
        counterBlack = 0
        counterWhite = 0
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i][j][0] == state.white:
                    counterWhite += 1
                if self.board[i][j][0] == state.whiteKing:
                    counterWhite += 1
                if self.board[i][j][0] == state.black:
                    counterBlack += 1
                if self.board[i][j][0] == state.blackKing:
                    counterBlack += 1
        return counterWhite, counterBlack

    def clearPawns(self):
        for i in range(0, 8):
            for j in range(0, 8):
                self.board[i][j][0] = state.empty

    def printBoard(self):
        for row in self.board:
            for element in row:
                print(element[1], end = ' ')
            print()