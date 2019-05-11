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

    def getPosition(self, color):
        toReturn = []
        for i in range(0, 8):
            for j in range(0, 8):
                if self.currentState[i][j] == color.value:
                    toReturn.append([i, j])
        
        return toReturn

