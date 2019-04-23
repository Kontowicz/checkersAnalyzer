import copy
from enum import  Enum
import os
import time
import cv2
from colorama import Fore, Back, Style
import numpy as np

class state(Enum):
    white = 1
    black = 2
    whiteKing = 3
    blackKing = 4
    empty = 0

class moveValidator:
    def __init__(self, debug, firstFieldColor=state.black):
        self.debug = debug
        self.currentColorMove = state.white
        self.previousState = None
        self.currentState = None
        self.data = []
        self.firstFieldColor = firstFieldColor

    def allInBlack(self):
        if self.firstFieldColor == state.black:
            # 0, 1 field is black
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
        isBeatPoss = self.isBeatPossible(colorMove)
        if self.debug:
            if isBeatPoss != False:
                print(Fore.RED + 'isBeatPossible: {}'.format(isBeatPoss))
                print(Style.RESET_ALL, end = '')        
            
        self.currentColorMove = self.toogleColorMove(self.currentColorMove)
        position = self.getDiffPosition(diff) 

        start = self.getStartPosition(position, colorMove)
        stop = self.getStopPosition(position)

        if start == None or stop == None:
            if self.debug:
                print('Invalid detection: start {} stop {}.'.format(start, stop))
                return False
            else:
                raise Exception('Invalid detection.')

        if self.previousState[start[0]][start[1]] == 1 or self.previousState[start[0]][start[1]] == 2:
            if len(position) == 2 and isBeatPoss == False:            
                return self.checkClassicMove(colorMove, start, stop)
            if len(position) == 3 and isBeatPoss != False:
                isBeatPoss = False
                beat = self.getBeatPosition(position, colorMove)
                return self.checkBeatMove(start, beat, stop, colorMove)
        if self.previousState[start[0]][start[1]] == 3 or self.previousState[start[0]][start[1]] == 4:
            if len(position) == 2 and isBeatPoss == False:            
                return self.checkKingMove(colorMove, start, stop)
            if len(position) == 3 and isBeatPoss != False:
                beat = self.getBeatPosition(position, colorMove)
                return self.checkKingBeat(colorMove, start, beat, stop)

        if self.debug:
            print('Invalid detection: {}'.format(position))
        else:
            raise Exception('Invalid detecion.')

    def getCurrentColorMoveKing(self, colorMove):
        if colorMove == state.white:
            return state.whiteKing
        return state.blackKing

    def getStartPosition(self, position, colorMove):
        king = self.getCurrentColorMoveKing(colorMove)

        for item in position:
            if self.previousState[item[0]][item[1]] == colorMove.value or self.previousState[item[0]][item[1]] == king.value:
                return item

    def getStopPosition(self, position):
        for item in position:
            if self.previousState[item[0]][item[1]] == state.empty.value:# or self.previousState[item[0]][item[1]] == king.value:
                return item

    def getBeatPosition(self, position, colorMove):
        beatPawnColor = self.toogleColorMove(colorMove)
        for item in position:
            if self.previousState[item[0]][item[1]] == beatPawnColor.value:
                return item

    def readNext(self, nextState):
        if self.currentState == None:
            self.currentState = copy.deepcopy(nextState)
            self.countPawns()
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
                if self.previousState[start[0]][start[1]] == self.currentState[stop[0]][stop[1]] or self.previousState[start[0]][start[1]] + 2 == self.currentState[stop[0]][stop[1]]:
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
                print('Color value: {}'.format(self.previousState[start[0]][start[1]]))
                if self.previousState[start[0]][start[1]] == self.currentState[stop[0]][stop[1]] or self.previousState[start[0]][start[1]] + 2 == self.currentState[stop[0]][stop[1]]:
                    beatPawnColor = self.toogleColorMove(colorMove)
                    if self.previousState[beat[0]][beat[1]] == beatPawnColor.value:
                        print('Valid beat color.')
                    else:
                        print('Invalid beat color.')
                else:
                    print('Invalid start stop colors1.')
                
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
                if self.previousState[start[0]][start[1]] == self.currentState[stop[0]][stop[1]] or self.previousState[start[0]][start[1]] + 2 == self.currentState[stop[0]][stop[1]]:
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
                if self.previousState[start[0]][start[1]] == self.currentState[stop[0]][stop[1]] or self.previousState[start[0]][start[1]] + 2 == self.currentState[stop[0]][stop[1]]:
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

    def checkKingMove(self, start, stop):
        if self.debug:
            right = []
            cnt = stop[1]
            for i in range(0, 8):
                right.append([i, cnt])
                cnt += 1
            left = []
            cnt = stop[1]
            for i in range(start[0], 8):
                right.append([i, cnt])
                cnt -= 1
            if stop not in right and stop not in left:
                print('Invalid king move.')
            else:
                print('Valid king move.')
        else:
            right = []
            cnt = stop[1]
            for i in range(0, 8):
                right.append([i, cnt])
                cnt += 1
            left = []
            cnt = stop[1]
            for i in range(0, 8):
                right.append([i, cnt])
                cnt -= 1
            if stop not in right and stop not in left:
                raise Exception('Invalid king move.')
            else:
                return True
            
    def checkKingBeat(self, colorMove, start, beat, stop):
        if self.debug:
            right = []
            cnt = start[1]
            for i in range(start[0] + 1, 8):
                cnt += 1
                right.append([i, cnt])

            cnt = start[1]
            for i in range(start[0] - 1, -1, -1):
                cnt -= 1
                right.append([i, cnt])


            left = []
            counter = point[1]
            for i in range(start[0] + 1, 8):
                counter -= 1
                left.append([i, cnt])

            counter = point[1]
            for i in range(start[0] - 1, -1, -1):
                counter += 1
                left.append([i, counter])

            print('Start: {} Stop: {}'.format(start, stop))
            print('Left: {} Right: {}'.format(left, right))
            if stop in right:
                if beat in right:
                    beatColor = self.toogleColorMove(colorMove)
                    if self.previousState[beat[0]][beat[1]] == beatColor.value:
                        print('Valid king beat.')
                        return True
            if stop in left:
                if beat in left:
                    beatColor = self.toogleColorMove(colorMove)
                    if self.previousState[beat[0]][beat[1]] == beatColor.value:
                        print('Valid king beat.')
                        return True
            print('Invalid king beat.')
            return False
        else:
            right = []
            cnt = start[1]
            for i in range(start[0] + 1, 8):
                cnt += 1
                right.append([i, cnt])

            cnt = start[1]
            for i in range(start[0] - 1, -1, -1):
                cnt -= 1
                right.append([i, cnt])


            left = []
            counter = point[1]
            for i in range(start[0] + 1, 8):
                counter -= 1
                left.append([i, cnt])

            counter = point[1]
            for i in range(start[0] - 1, -1, -1):
                counter += 1
                left.append([i, counter])

            if stop in right:
                if beat in right:
                    beatColor = self.toogleColorMove(colorMove)
                    if self.previousState[beat[0]][beat[1]] == beatColor.value:
                        return True
            if stop in left:
                if beat in left:
                    beatColor = self.toogleColorMove(colorMove)
                    if self.previousState[beat[0]][beat[1]] == beatColor.value:
                        return True
            raise Exception('Invalid king beat.')

    def isBeatPossible(self, colorMove):
        toReturn = []
        for i in range(0, 8):
            for j in range(0, 8):
                if colorMove == state.white:
                    if self.previousState[i][j] == state.white.value:
                        if i + 2 < 8 and j + 2 < 8:
                            if self.previousState[i+1][j+1] == state.black.value and self.previousState[i+2][j+2] == state.empty.value:
                                toReturn.append([i, j])

                        if i + 2 < 8 and j - 2 >= 0:
                            if self.previousState[i+1][j-1] == state.black.value and self.previousState[i+2][j-2] == state.empty.value:
                                toReturn.append([i, j])  

                if colorMove == state.black:
                    if self.previousState[i][j] == state.black.value:
                        if i - 2 >= 0 and j + 2 < 8:
                            if self.previousState[i-1][j+1] == state.white.value and self.previousState[i-2][j+2] == state.empty.value:
                                toReturn.append([i, j])
                        if i - 2 >= 0 and j - 2 >= 0:
                            if self.previousState[i-1][j-1] == state.white.value and self.previousState[i-2][j-2] == state.empty.value:
                                toReturn.append([i, j])           
        if toReturn != []:
            return toReturn
        return False

    def countPawns(self):
        white = 0
        black = 0
        for i in self.currentState:
            for j in i:
                if j == state.white.value:
                    white += 1
                if j == state.black.value:
                    black += 1
        
        if black != 12 or white != 12:
            if self.debug:
                print('Invalid pawn ammount.')
                return False
            else:
                raise Exception('Invalid pawn ammount.')

        return True

    # For testing
    def runAllTests(self):
        files = os.listdir('testCases/firstFieldBlack')
        for file in files:
            try:
                self.currentColorMove = state.black
                self.previousState = None
                self.currentState = None
                self.data = []
                print(file)
                self.test('./testCases/firstFieldBlack/'+file)
                print('All move valid.')
            except Exception as e:
                print(e)
            print()

        files = os.listdir('testCases/firstFieldWhite')
        for file in files:
            try:
                self.currentColorMove = state.white
                self.previousState = None
                self.currentState = None
                self.data = []
                print(file)
                self.test('./testCases/firstFieldWhite/'+file)
                print('All move valid.')
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

    def getBoard(self):
        img = np.zeros((544,544, 3), dtype=np.uint8)
        c = np.fromfunction(lambda x, y: ((x // 68) + (y // 68)) % 2, (544, 544))
        
        if self.firstFieldColor == state.black:
            img[c == 0] = (0,0,0)
            img[c == 1] = (255,255,255)
        else:
            img[c == 0] = (255,255,255)
            img[c == 1] = (0,0,0)
        
        white = self.getPosition(state.white)
        black = self.getPosition(state.black)
        blackKing = self.getPosition(state.blackKing)
        whiteKing = self.getPosition(state.whiteKing)



        for item in white:
            cv2.circle(img, ((((item[1] + 1) * 68) - 34), (((item[0] + 1) * 68) - 34)), 20, (217,217,217), -1)

        for item in black:
            cv2.circle(img, ((((item[1] + 1) * 68) - 34), (((item[0] + 1) * 68) - 34)), 20, (100, 100, 100), -1)

        for item in blackKing:
            cv2.circle(img, ((((item[1] + 1) * 68) - 34), (((item[0] + 1) * 68) - 34)), 20, (100, 100, 100), -1)
            cv2.circle(img, ((((item[1] + 1) * 68) - 34), (((item[0] + 1) * 68) - 34)), 10, (1,1,1), -1)

        for item in whiteKing:
            cv2.circle(img, ((((item[1] + 1) * 68) - 34), (((item[0] + 1) * 68) - 34)), 20, (217,217,217), -1)
            cv2.circle(img, ((((item[1] + 1) * 68) - 34), (((item[0] + 1) * 68) - 34)), 10, (256,256,256), -1)
        
        return img

    def getPosition(self, color):
        toReturn = []
        for i in range(0, 8):
            for j in range(0, 8):
                if self.currentState[i][j] == color.value:
                    toReturn.append([i, j])
        
        return toReturn

    def visualization(self, fileName):
        self.readData(fileName)
        for i in range(0, len(self.data)):
            self.readNext(self.data[i])
            self.checkMove()
            img = self.getBoard()
            cv2.imshow(fileName, img)
            cv2.waitKey(2000)
        
if __name__ == "__main__":        
    mv = moveValidator(False)
    mv.test('testCases/firstFieldBlack/validKingBeat.txt')
    #mv.test('testCases/allMoveValid.txt')
    # try:
    #     mv.runAllTests()
    # except Exception as e:
    #     print(e)