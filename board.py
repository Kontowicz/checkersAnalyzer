from enum import  Enum

class color(Enum):
    white = 1
    black = 2
    empty = 0

class board(object):
    def __init__(self, firstColor, sq):
        #self.coordinates.update({str(x) + str(y): [self.sq * (x + 1), self.sq * (y + 1)]})
        self.board = []
        for i in range(0, 8):
            tmp = []
            for i in range(0,8):
                tmp.append([color.empty, color.black, [0, 0]])
            self.board.append(tmp)

        for i in range(0, 8):
            for j in range(0, 8):
                self.board[i][j][2] = [(i + 1) * sq, (j + 1) * sq]

        self.setFieldsColor(firstColor)


    def setFieldsColor(self, firstFieldColor):
        firstColor = color.black
        secondColor = color.white

        if firstFieldColor == color.white:
            firstColor = color.white
            secondColor = color.black

        for i in range(0, 8):
            for j in range(0, 8):
                if j % 2 == 0:
                    self.board[i][j][1] = firstColor
                else:
                    self.board[i][j][1] = secondColor


    def setFieldCord(self, x, y, cord = []):
        self.board[x][y][2] = cord

    def setPawnColor(self, x, y, color):
        self.board[x][y][0] = color

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
                if self.board[i][j][0] == color.white:
                    counterWhite += 1
                if self.board[i][j][0] == color.black:
                    counterBlack += 1
        return counterWhite, counterBlack

    def clearPawns(self):
        for i in range(0, 8):
            for j in range(0, 8):
                self.board[i][j][0] = color.empty