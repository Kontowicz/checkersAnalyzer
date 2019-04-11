import copy
from enum import  Enum

class state(Enum):
    white = 1
    black = 2
    empty = 0

class moveValidator:
    previousState: None

    def __init__(self, debug):
        self.debug = debug
        self.currentColorMove = state.white
        file = open('dupm.txt', 'w')
        file.close()
        self.previousState = None
        self.currentState = None
        self.data = []

    def readData(self):
        file = open('test.txt', 'r')
        data = file.read()
        data = data.split('\n')
        lineTMP = []
        table = []
        for line in data:
            if line == '':
                self.data.append(table)
                table = []
                continue
            lineTMP = []
            for item in line:
                if item != ' ':
                    lineTMP.append(int(item))
            table.append(lineTMP)

    def toogleColorMove(self, color):
        if color == state.black:
            return state.white
        return state.black

    def checkMove(self):
        diff = self.getDiff()

        if diff == None:
            return True

        colorMove = self.currentColorMove
        self.currentColorMove = self.toogleColorMove(self.currentColorMove)
        position = self.getDiffPosition(diff) 

        if len(position) == 2:            
            a0 = position[0][0]
            a1 = position[0][1]
            a2 = position[1][0]
            a3 = position[1][1]
            
            if ((self.previousState[a0][a1] == self.currentState[a2][a3]) or (self.currentState[a0][a1] == self.previousState[a2][a3])) or self.previousState[a0][a1] == colorMove.value or self.currentState[a2][a3] == colorMove.value or self.currentState[a0][a1] == colorMove.value or self.previousState[a2][a3] == colorMove.value:
                
                self.checkClassicMove(position)
            else:
                raise 'Invalid'
        if len(position) == 3:
            self.checkBeatMove(position)

    def readNext(self, nextState):
        if self.currentState == None:
            self.currentState = copy.deepcopy(nextState)
        if self.currentState != None:
            self.previousState = copy.deepcopy(self.currentState)
            self.currentState = copy.deepcopy(nextState)

    def test(self):
        self.readData()
        self.readNext(self.data[0])
        diff = self.getDiff()
        for i in range(1, len(self.data)):
            self.readNext(self.data[i])
            self.checkMove()

    def getDiff(self):
        toReturn = []
        wasDiff = False
        for i in range(0, 8):
            tmp = []
            for j in range(0, 8):
                if self.currentState[i][j] != self.previousState[i][j]:
                    wasDiff = True
                    tmp.append(1)
                else:
                    tmp.append(0)
            toReturn.append(tmp)

        if wasDiff:
            return toReturn

        return None

    def checkClassicMove(self, position):
        if self.debug:
            first = []
            second = []
            for item in position:
                first.append(item[0])
                second.append(item[1])

            first.sort()
            second.sort()
            if first[0] + 1 == first[1] and second[0] + 1 == second[1]:
                print('Valid move')
            else:
                print('Invalid move')
        else:
            first = []
            second = []
            for item in position:
                first.append(item[0])
                second.append(item[1])

            first.sort()
            second.sort()
            if first[0] + 1 == first[1] and second[0] + 1 == second[1]:
                print('Valid move')
            else:
                raise 'Invalid move'

    def checkBeatMove(self, position):
        if self.debug:
            first = []
            second = []
            for item in position:
                first.append(item[0])
                second.append(item[1])

            first.sort()
            second.sort()

            if first[0] + 1 == first[1] and first[1] + 1 == first[2]:
                if second[0] + 1 == second[1] and second[1] + 1 == second[2]:
                    print('Valid beat')
                else:
                    print('Invalid beat')
        else:
            first = []
            second = []
            for item in position:
                first.append(item[0])
                second.append(item[1])

            first.sort()
            second.sort()

            if first[0] + 1 == first[1] and first[1] + 1 == first[2]:
                if second[0] + 1 == second[1] and second[1] + 1 == second[2]:
                    print('Valid beat')
                else:
                    raise 'Invalid move'

    def getDiffPosition(self, diff):
        position = []

        for i in range(0, 8):
            for j in range(0, 8):
                if diff[i][j] == 1:
                    position.append([i, j])
        
        return position

    def dumpToFile(self, diff):
        file = open('dump.txt', 'a')

        file.write('previousState\n')
        for item in self.previousState:
            for elem in item:
                file.write('{} '.format(elem))
            file.write('\n')

        file.write('\ncurrentState\n')
        for item in self.currentState:
            for elem in item:
                file.write('{} '.format(elem))
            file.write('\n')
        file.write('\n')
        
        file.write('diff\n')
        for item in diff:
            for elem in item:
                file.write('{} '.format(elem))
            file.write('\n')
        file.close()

if __name__ == "__main__":
    mv = moveValidator(True)
    mv.test()