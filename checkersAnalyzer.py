import cv2
import numpy as np
import copy
import board
import time
from board import state as color
import moveValidator

class checkersAnalyzer(object):

    # Constructor
    # Now i assume that black pawns are always at the board bottom.
    def __init__(self, debug, img):
        self.moveValid = moveValidator.moveValidator(debug)

        self.debug = debug
        self.counter = 0
        self.currentColorMove = color.white # TODO: change color in when captured game start with white pawn move
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
        self.param1 = 40
        self.param2 = 40
        self.min = 20
        self.max = 24

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

    # Pass arguments for display image, join displayed image with board.
    def drawBoard(self):
        return self.image_circle, self.image, self.board

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
    def detectCircle(self, nextto):

        def detectKing(image, white, width_sq, height_sq):
            centerking = []
            if white:
                kernel = np.ones((5, 5), np.uint8)
                lower = np.array([20, 100, 100])
                uper = np.array([50, 255, 255])
                img_hsv2 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                mask_one = cv2.inRange(img_hsv2, lower, uper)
                morphology = cv2.morphologyEx(mask_one, cv2.MORPH_OPEN, kernel)
                morphology = cv2.morphologyEx(morphology, cv2.MORPH_DILATE, kernel)
                _, contours, _ = cv2.findContours(morphology, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                if contours is not None:
                    for x in contours:
                        M = cv2.moments(x)
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        cx = int(cx // width_sq)
                        cy = int(cy // height_sq)
                        centerking.append([cx,cy])
            else:
                kernel = np.ones((5, 5), np.uint8)
                lower = np.array([160, 100, 100])
                uper = np.array([179, 255, 255])
                img_hsv2 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                mask_one = cv2.inRange(img_hsv2, lower, uper)
                morphology = cv2.morphologyEx(mask_one, cv2.MORPH_OPEN, kernel)
                morphology = cv2.morphologyEx(morphology, cv2.MORPH_DILATE, kernel)
                _, contours, _ = cv2.findContours(morphology, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                if contours is not None:
                    for x in contours:
                        M = cv2.moments(x)
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        cx = int(cx // width_sq)
                        cy = int(cy // height_sq)
                        centerking.append([cx,cy])
            return centerking

        img = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        self.image_circle = self.image.copy()

        # Calculate field width based on current image.
        width_sq = img.shape[0] / 8
        height_sq =  img.shape[1] / 8

        # Detect circles in image.
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, 40, param1=self.param1, param2=self.param2, minRadius=self.min, maxRadius=self.max)
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

        white = detectKing(self.image,True,width_sq,height_sq)
        black = detectKing(self.image, False, width_sq, height_sq)

        for KingWhite in white:
            self.currentStateBoard.setPawnColor(KingWhite[1], KingWhite[0], color.whiteKing)
            i, j = self.currentStateBoard.getFieldCord(KingWhite[1], KingWhite[0])
            cv2.circle(self.board, (j - 34, i - 34), 20, (217, 217, 217), -1)
            cv2.circle(self.board, (j - 34, i - 34), 10, (201, 232, 0), -1)

        for KingBlack in black:
            self.currentStateBoard.setPawnColor(KingBlack[1], KingBlack[0], color.blackKing)
            i, j = self.currentStateBoard.getFieldCord(KingBlack[1], KingBlack[0])
            cv2.circle(self.board, (j - 34, i - 34), 20, (64, 64, 64), -1)
            cv2.circle(self.board, (j - 34, i - 34), 10, (201, 232, 0), -1)

        self.TestBoard()

        if self.counter == 0:
            self.previousStateBoard.board = copy.deepcopy(self.currentStateBoard.board)
            self.counter = 1
        b = self.getBoard()
        if nextto == True:
            self.moveValid.readNext(b)

    def checkMove(self):
        self.moveValid.checkMove()

    def getBoard(self):
        toReturn = []
        for item in self.previousStateBoard.board:
            tmp = []
            for elem in item:
                tmp.append(elem[0].value)
            toReturn.append(tmp)

        return toReturn

    def TestBoard(self):
        toReturn = []
        for item in self.previousStateBoard.board:
            tmp = []
            for elem in item:
                tmp.append(elem[0].value)
            toReturn.append(tmp)

        print("**"*10,'\n',toReturn,'\n')

