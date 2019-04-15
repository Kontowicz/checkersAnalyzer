import copy
from enum import  Enum
import os

class state(Enum):
    white = 1
    black = 2
    empty = 0

class moveValidator:
    def __init__(self, debug, firstFieldColor=state.white):
        self.debug = debug
        self.currentColorMove = state.white
        self.previousState = None
        self.currentState = None
        self.data = []
        self.firstFieldColor = firstFieldColor

    def allInBlack(self):
    # 0, 1 field is black
        if self.firstFieldColor == state.black:
            for i in range(0, 8):
                if i % 2 == 1:
                    for j in range(0, 8, 2):
                        if self.currentColorMove[i][j] != 0:
                            return False
                        #print('I: {} J: {}'.format(i, j))
                else:
                    for j in range(1, 8, 2):
                        if self.currentColorMove[i][j] != 0:
                            return False                    
                        #print('I: {} J: {}'.format(i, j))
        else:
            # 0, 0 field is black
            for i in range(0, 8):
                if i % 2 != 1:
                    for j in range(0, 8, 2):
                        if self.currentColorMove[i][j] != 0:
                            return False                    
                        #print('I: {} J: {}'.format(i, j))
                else:
                    for j in range(1, 8, 2):
                        if self.currentColorMove[i][j] != 0:
                            return False                    
                        #print('I: {} J: {}'.format(i, j))
        return True

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

        start = self.getStartPosition(position, colorMove)
        stop = self.getStopPosition(position)

        if self.debug:
            print('Start: {} stop: {}'.format(start, stop))

        if len(position) == 2:            
            return self.checkClassicMove(colorMove, start, stop)
        if len(position) == 3:
            beat = self.getBeatPosition(position, colorMove)
            return self.checkBeatMove(start, beat, stop, colorMove)

        if self.debug:
            print('Invalid detection')
        else:
            raise Exception('Invalid detecion.')

    def getStartPosition(self, position, colorMove):
        for item in position:
            if self.previousState[item[0]][item[1]] == colorMove.value:
                return item

    def getStopPosition(self, position):
        for item in position:
            if self.previousState[item[0]][item[1]] == state.empty.value:
                return item

    def getBeatPosition(self, position, colorMove):
        beatPawnColor = self.toogleColorMove(colorMove)
        for item in position:
            if self.previousState[item[0]][item[1]] == beatPawnColor.value:
                return item

    def readNext(self, nextState):
        if self.currentState == None:
            self.currentState = copy.deepcopy(nextState)
        if self.currentState != None:
            self.previousState = copy.deepcopy(self.currentState)
            self.currentState = copy.deepcopy(nextState)

    def getDiff(self):

        try:
            if self.currentState == [] or self.previousState == []:
                return None

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
        except:
            print('dataLen: {}'.format(len(self.data)))
            for item in self.currentState:
                print(item)
            print('prevState')
            for item in self.previousState:
                print(item)

    def checkClassicMove(self, colorMove, start, stop):
        if self.debug:
            if self.previousState[start[0]][start[1]] != self.currentState[stop[0]][stop[1]]:
                print('Invalid colors.')
            if colorMove == state.white:
                if stop in [[start[0] + 1, start[1] - 1], [start[0] + 1, start[1] + 1]]:
                    print('Valid move white.')
                else:
                    print('Invalid move white.')
            else:
                if stop in [[start[0] - 1, start[1] - 1], [start[0] - 1, start[1] + 1]]:
                    print('Valid move black.')
                else:
                    print('Invalid move black.')
        else:
            if self.previousState[start[0]][start[1]] != self.currentState[stop[0]][stop[1]]:
                raise Exception('Invalid pawn color.')
            if colorMove == state.white:
                if stop in [[start[0] + 1, start[1] - 1], [start[0] + 1, start[1] + 1]]:
                    return True
                else:
                    raise Exception('Invalid move white.')
            else:
                if stop in [[start[0] - 1, start[1] - 1], [start[0] - 1, start[1] + 1]]:
                    return True
                else:
                    raise Exception('Invalid move black.')

    def checkBeatMove(self, start, beat, stop, colorMove):
        if self.debug:
            if colorMove == state.white:
                if self.previousState[start[0]][start[1]] == self.currentState[stop[0]][stop[1]]:
                    beatPawnColor = self.toogleColorMove(colorMove)
                    if self.previousState[beat[0]][beat[1]] == beatPawnColor.value:
                        print('Valid beat color.')
                    else:
                        print('Invalid beat color.')
                else:
                    print('Invalid start stop colors.')
                
                if beat[0] == start[0] + 1 and beat[1] == start[1] + 1:
                    if stop[0] == beat[0] + 1 and stop[1] == beat[1] + 1:
                        print('Valid beat white.')
                        return True

                if beat[0] == start[0] + 1 and beat[1] == start[1] - 1:
                    if stop[0] == beat[0] + 1 and stop[1] == beat[1] - 1:
                        print('Valid beat white.')
                        return True
                print('Invalid beat white.')
                return False
            if colorMove == state.black:
                if self.previousState[start[0]][start[1]] == self.currentState[stop[0]][stop[1]]:
                    beatPawnColor = self.toogleColorMove(colorMove)
                    if self.previousState[beat[0]][beat[1]] == beatPawnColor.value:
                        print('Valid beat color.')
                    else:
                        print('Invalid beat color.')
                else:
                    print('Invalid start stop colors.')
                
                if beat[0] == start[0] - 1 and beat[1] == start[1] + 1:
                    if stop[0] == beat[0] - 1 and stop[1] == beat[1] + 1:
                        print('Valid beat white.')
                        return True

                if beat[0] == start[0] - 1 and beat[1] == start[1] - 1:
                    if stop[0] == beat[0] - 1 and stop[1] == beat[1] - 1:
                        print('Valid beat white.')
                        return True
                print('Invalid beat white.')
                return False
        else:
            if colorMove == state.white:
                if self.previousState[start[0]][start[1]] == self.currentState[stop[0]][stop[1]]:
                    beatPawnColor = self.toogleColorMove(colorMove)
                    if self.previousState[beat[0]][beat[1]] == beatPawnColor.value:
                        return True
                        print('Valid beat color.')
                    else:
                        raise Exception('Invalid beat color.')
                else:
                    raise Exception('Invalid start stop colors.')
                
                if beat[0] == start[0] + 1 and beat[1] == start[1] + 1:
                    if stop[0] == beat[0] + 1 and stop[1] == beat[1] + 1:
                        return True

                if beat[0] == start[0] + 1 and beat[1] == start[1] - 1:
                    if stop[0] == beat[0] + 1 and stop[1] == beat[1] - 1:
                        return True

                raise Exception('Invalid beat white.')
            if colorMove == state.black:
                if self.previousState[start[0]][start[1]] == self.currentState[stop[0]][stop[1]]:
                    beatPawnColor = self.toogleColorMove(colorMove)
                    if self.previousState[beat[0]][beat[1]] == beatPawnColor.value:
                        return True
                        print('Valid beat color.')
                    else:
                        raise Exception('Invalid beat color.')
                else:
                    raise Exception('Invalid start stop colors.')
                
                if beat[0] == start[0] - 1 and beat[1] == start[1] + 1:
                    if stop[0] == beat[0] - 1 and stop[1] == beat[1] + 1:
                        return True

                if beat[0] == start[0] - 1 and beat[1] == start[1] - 1:
                    if stop[0] == beat[0] - 1 and stop[1] == beat[1] - 1:
                        return True

                raise Exception('Invalid beat white.')

    def getDiffPosition(self, diff):
        position = []
        for i in range(0, 8):
            for j in range(0, 8):
                if diff[i][j] == 1:
                    position.append([i, j])
        
        return position

    # For testing
    def runAllTests(self):
        files = os.listdir('testCases')
        for file in files:

            try:
                self.currentColorMove = state.white
                self.previousState = None
                self.currentState = None
                self.data = []
                print(file)
                self.test('./testCases/'+file)
                
            except Exception as e:
                print(e)
            print()

    def test(self, fileName):
        self.readData(fileName)

        for i in range(0, len(self.data)):
            self.readNext(self.data[i])
            self.checkMove()

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

    def writeToFile(self):        
        file_current = open('currentState.txt', 'w')
        file_prev = open('prevState.txt', 'w')
        for i in range(0, len(self.data) - 1):
            tmp = self.getDiffTmp(self.data[i], self.data[i+1])
            if tmp != None:
                print(tmp)
                for item in self.data[i]:
                    for elem in item:
                        file_current.write('{} '.format(elem))
                    file_current.write('\n')
                file_current.write('\n')

                for item in self.data[i+1]:
                    for elem in item:
                        file_prev.write('{} '.format(elem))
                    file_prev.write('\n')
                file_prev.write('\n')                
            
        file_current.close()
        file_prev.close()

    def readData(self, fileName):
        file = open(fileName, 'r')
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


if __name__ == "__main__":        
    mv = moveValidator(False)
    try:
        mv.runAllTests()
    except Exception as e:
        print(e)