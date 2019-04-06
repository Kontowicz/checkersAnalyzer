import cv2
import numpy as np
import copy
import board
from board import state as color

class checkersAnalyzer(object):

    # Constructor
    # Now i assume that balck pawns are always at the board bottom.
    def __init__(self, debug, img):
        self.debug = debug
        file = open('test.txt', 'w')
        file.close()
        self.counter = 0
        self.bootomPawnColor = None
        self.currentColorMove = color.black # TODO: change color in when captured game start with white pawn move
        self.image = img # Image captured from camera
        self.points = [] # Points for transposition
        self.wh_size= 450 # Widht, heigt image for work
        self.sq = 68 # Field size
        self.checkers_size = 544 # Board size for visualisation
        self.board = None # Board visualisation
        self.first_sq = None
        self.detectAreaBoardDistribution()
        self.currentStateBoard = board.board(self.first_sq, self.sq)
        self.previousStateBoard = board.board(self.first_sq, self.sq)

    def analyze(self):
#TODO: Move functionality from main file -> main file should look like: checkAnalyzer = checkersAnalyzer.checkersAnalyzer(); checkAnalyzer.run()
        raise NotImplemented()


    def isValidBoard(self):
        raise NotImplemented()

    # Set frame as image.
    def readVideo(self,img):
        self.image=cv2.resize(img,(self.wh_size,self.wh_size))

    # Read image.
    def read(self, path1):
        self.image = cv2.imread(path1, cv2.IMREAD_COLOR)
        self.image = cv2.resize(self.image, (self.wh_size,self.wh_size))

    # Morphological transposiotin to get board based on previwious parematers.
    def checkboardTransposition(self):
        p = self.points
        pts1 = np.float32([[p[0][0], p[0][1]], [p[1][0], p[1][1]], [p[2][0], p[2][1]], [p[3][0], p[3][1]]])
        pts2 = np.float32([[0, 0], [self.wh_size, 0], [self.wh_size, self.wh_size], [0, self.wh_size]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(self.image, M, (self.wh_size, self.wh_size))
        self.image = dst

    # Get board position by hand
    def checkboardCoordinate(self):
        def onMouse(event, x, y,flaga,a):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.points.append([x,y])
        cv2.imshow('Wejściowy obraz', self.image)
        cv2.setMouseCallback('Wejściowy obraz', onMouse)
        while len(self.points)<4:
            cv2.waitKey(1)

    # Create board for visualisation.
    def createCheckers(self):
        img = np.zeros((self.checkers_size,self.checkers_size, 3), dtype=np.uint8)
        c = np.fromfunction(lambda x, y: ((x // self.sq) + (y // self.sq)) % 2, (self.checkers_size, self.checkers_size))
        if self.first_sq == color.black:
            img[c == 0] = (0,0,0)
            img[c == 1] = (255,255,255)
        else:
            img[c == 0] = (255,255,255)
            img[c == 1] = (0,0,0)
        return img

    # Draw current pawn state.
    def drawTextInImageText(self):
        text = np.zeros((136,self.checkers_size, 3), dtype=np.uint8)
        text[::]=(128,128,128)
        black, white = self.currentStateBoard.countPawns()
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(text, 'Biale: ' + str(white), (150, 60), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(text, 'Czarne: ' + str(black), (110, 125), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
        return text

    # Pass arguments for display image, join displayed image with board.
    def drawBoard(self):
        new_board = np.concatenate((self.board,self.drawTextInImageText()),axis=0)
        return self.image_circle, self.image, new_board
        cv2.imshow('Zaznaczone pionki', self.image_circle)
        cv2.imshow('Plansza', self.image)
        cv2.imshow('Wizualizacja', new_board)

    # Detect fields distribution.
    def detectAreaBoardDistribution(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        width, height = [x // 8 for x in img.shape[0:2]]

        cut_area = img[width*3:width*4,height:width*2]

        thresh = cv2.threshold(cut_area, 175, 255, cv2.THRESH_BINARY)[1]

        if thresh[width//2,height//2]==0:
            self.first_sq = color.black
        else:
            self.first_sq = color.white

    # Detect pawns.
    def detectCircle(self):
        img = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        self.image_circle = self.image.copy()

        # Calculate field width based on current image.
        width_sq = img.shape[0] / 8
        height_sq =  img.shape[1] / 8

        # Detect circles in image.
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, 40, param1=100, param2=30, minRadius=18, maxRadius=22)
        circles = np.uint16(np.around(circles))

        # Select detected circle center and it's  contours
        for i in circles[0, :]:
            cv2.circle(self.image_circle, (i[0], i[1]), i[2], (0, 255, 0), 1);
            cv2.circle(self.image_circle, (i[0], i[1]), 2, (0, 0, 255), 3);

        matrix2 = []  # Table for storage pawns positions.
        center_circle = [] # Table for storage image slices with circle center.

        # Fill matrix2 and center_circle
        for x in circles[0]:
            x1 = int(x[1] // width_sq)
            y1 = int(x[0] // height_sq)
            cut_area = img[x[1] - 5:x[1] + 5, x[0] - 5:x[0] + 5]
            ret, thresh1 = cv2.threshold(cut_area, 160, 255, cv2.THRESH_BINARY)
            center_circle.append(thresh1)
            matrix2.append([y1, x1])

        # Update currentStateBoard and draw conturs.
        self.board = self.createCheckers()
        self.previousStateBoard.board = copy.deepcopy(self.currentStateBoard.board)
        self.currentStateBoard.clearPawns()
        for x, y in zip(matrix2, center_circle):
            if y[4,4]==0:
                self.currentStateBoard.setPawnColor(x[1], x[0], color.black)
                i, j = self.currentStateBoard.getFieldCord(x[1], x[0])
                cv2.circle(self.board, (j - 34, i - 34), 20, (64,64,64), -1)
            else:
                self.currentStateBoard.setPawnColor(x[1], x[0], color.white)
                i, j = self.currentStateBoard.getFieldCord(x[1], x[0])
                cv2.circle(self.board, (j - 34, i - 34), 20, (217,217,217), -1)

        if self.counter == 0:
            self.previousStateBoard.board = copy.deepcopy(self.currentStateBoard.board)
        
        self.counter = 1
        self.getDiff()
        self.checkMoves()
        # if self.checkMoves():
        #     self.currentColorMove = color.black if self.currentColorMove == color.white else color.white
        #     print('Next move pawn color: {}'.format(self.currentColorMove))

    def isValidMove(self):
        raise NotImplemented()

    def checkMoves(self):
        self.allInBlack()
        file = open('test.txt', 'a')
        diff = self.getDiff()
        if diff == None:
            return None

        tmp = []
        for i in range(0, 8):
            for j in range(0, 8):
                if diff[i][j] == 1:
                    file.write('1 ')
                    tmp.append([i, j])
                else:
                    file.write('0 ')
            file.write('\n')
        file.write('\n')
        file.write('\n')
        file.close()
        if len(tmp) == 1:
            return None

        # GET START POSITON
        startPos = [0,0]
        for item in tmp:
            if self.previousStateBoard.getPawnColor(item[0],item[1]) == self.currentColorMove:
                startPos = item

        # GET END POSITION
        stopPos = [0,0]
        for item in tmp:
            if self.previousStateBoard.getPawnColor(item[0],item[1]) == color.empty:
                stopPos = item

        if self.currentColorMove != self.currentStateBoard.board[stopPos[0]][stopPos[1]][0]:
            print('Current color move: {} Detected move: {}'.format(self.currentColorMove, self.currentStateBoard.getPawnColor(stopPos[0], stopPos[1]))) 
            #raise 'Invalid move'
        
        if len(tmp) == 1:
            if self.debug:
                print('Invalid detection: {}'.format(len(tmp)))
            else:
                raise 'Invalid detection'
        
        if len(tmp) == 2:
            if self.debug:
                if self.currentStateBoard.getPawnColor(stopPos[0], stopPos[1]) != self.previousStateBoard.getPawnColor(startPos[0], startPos[1]):
                    if self.debug:
                        print('Invalid detection: {}'.format(tmp))
                    else:
                        raise 'Invalid detection'

                if self.currentColorMove == color.white:
                    if stopPos in [[startPos[0] + 1, startPos[1] - 1], [startPos[0] + 1, startPos[1] + 1]]:
                        print('Valid move white')
                elif self.currentColorMove == color.black:
                    if stopPos in [[startPos[0] - 1, startPos[1] - 1], [startPos[0] - 1, startPos[1] + 1]]:
                        print('Valid move black')
            else:
                raise 'Invalid move'
        if len(tmp) == 3:
            if self.debug:
                # Find start position
                beatPawnPos = [0, 0]
                secondColor = color.black if self.currentColorMove == color.white else color.white # Toggle collors
                for item in tmp:
                    if self.previousStateBoard.getPawnColor(item[0],item[1]) == secondColor:
                        beatPawnPos = item
                print('Beat pos: {} Przewidywany kolor: {} Znaleziony kolor: {}'.format(beatPawnPos, secondColor, self.previousStateBoard.getPawnColor(beatPawnPos[0],beatPawnPos[1])))
            else:
                raise 'Invalid move'
        if len(tmp) > 3:
            if self.debug:
                print('Invalid detection: {}'.format(len(tmp)))
            else:
                raise 'Invalid detection'

        self.currentColorMove = color.black if self.currentColorMove == color.white else color.white # Toggle collors

        return True
        

    def allInBlack(self):
        for item in self.currentStateBoard.board:
            for element in item:
                if element[0] is not color.empty and element[1] is color.white:
                    raise 'Invalid position'

    def getDiff(self):
        toReturn = []
        wasDiff = False
        for i in range(0, 8):
            tmp = []
            for j in range(0, 8):
                if self.currentStateBoard.board[i][j][0] != self.previousStateBoard.board[i][j][0]:
                    wasDiff = True
                    tmp.append(1)
                else:
                    tmp.append(0)
            toReturn.append(tmp)

        if wasDiff:
            return toReturn
            for item in toReturn:
                for elem in item:
                    print(elem, end = ' ')
                print()

        return None
