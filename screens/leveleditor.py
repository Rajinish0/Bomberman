from .screen import Screen
from screens.GameWindow import GameWindow
from constants import *
from button import Button
from gameObjects import *
from utils import *
import pygame
from copy import deepcopy

'''
TEMPORARY CLASS FOR EXPERIMENTATION PURPOSES.
'''

# For all the images
imgs = {
    BOX: Box.image,
    WALL: Wall.image,
    EMPTY: EmptySpace.image,
    PLAYER1 : "sprites/players/Gamer1.png",
    PLAYER2 : "sprites/players/Gamer2.png",
    BASE_MONSTER : "sprites/monsters/m1.jpg",
    GHOST_MONSTER : "sprites/monsters/m1.jpg",
    FAST_MONSTER : "sprites/monsters/m1.jpg",
    PSEUDOINTELLIGENT_MONSTER : "sprites/monsters/m1.jpg"
}

# The surrounding borders
borders = [0, NUM_BOXES - 1]


# Checks whether the mouse click was within a rectangular grid or not
def inBound(x, y, lx, ly, w, h):
    return (lx <= x <= lx + w and
            ly <= y <= ly + h)


# Converts the co-ordinates of the mouse click to indices of the grid
def ScreenCrdToIdx(x, y, width, height):
    return (y // height, x // width)

class LevelEditor(Screen):

    def __init__(self):
        self.offSetX = 200
        self.offSetY = 0
        self.boxWidth = (W - self.offSetX) // NUM_BOXES
        self.boxHeight = (H - self.offSetY) // NUM_BOXES
        self.grid = [[EMPTY for i in range(NUM_BOXES)]
                     for j in range(NUM_BOXES)]
        self.backButton = Button(
            10, 10, 30, 30, text="Back",
            callBack=lambda: self.gameMgr.setState(
                self.gameMgr.getPrevState(),
            ),
            center=False
        )
        self.boxButton = Button(
            80, 20, self.boxWidth, self.boxHeight, img=Box.image,
            callBack=lambda: self.setSelected(BOX),
            center=False
        )

        self.wallButton = Button(
            80, 80, self.boxWidth, self.boxHeight, img=Wall.image,
            callBack=lambda: self.setSelected(WALL),
            center=False
        )

        self.emptyButton = Button(
            80, 140, self.boxWidth, self.boxHeight, img=EmptySpace.image,
            callBack=lambda: self.setSelected(EMPTY),
            center=False
        )

        self.P1Button = Button(
            80, 200, self.boxWidth, self.boxHeight, img="sprites/players/Gamer1.png",
            callBack=lambda:self.setSelected(PLAYER1),
            center=False
        )

        self.P2Button = Button(
            80, 260, self.boxWidth, self.boxHeight, img="sprites/players/Gamer2.png",
            callBack=lambda:self.setSelected(PLAYER2),
            center=False
        )

        self.baseMButton = Button(
            80, 320, self.boxWidth, self.boxHeight, img="sprites/monsters/m1.jpg",
            callBack=lambda: self.setSelected(BASE_MONSTER),
            center=False
        )

        self.ghostMButton = Button(
            80, 380, self.boxWidth, self.boxHeight, img="sprites/monsters/m1.jpg",
            callBack=lambda: self.setSelected(GHOST_MONSTER),
            center=False
        )

        self.fastMButton = Button(
            80, 440, self.boxWidth, self.boxHeight, img="sprites/monsters/m1.jpg",
            callBack=lambda: self.setSelected(FAST_MONSTER),
            center=False
        )

        self.pseudoIntMButton = Button(
            80, 500, self.boxWidth, self.boxHeight, img="sprites/monsters/m1.jpg",
            callBack=lambda: self.setSelected(PSEUDOINTELLIGENT_MONSTER),
            center=False
        )

        self.resetButton = Button(
            x=80, y=550, width=200, height=100,
            callBack=lambda: self.reset(),
            center=False,
            text="Reset Map",
            textSize=15,
            textColor=BLACK,
        )

        self.startButton = Button(
            x=80, y=580, width=200, height=100,
            callBack=lambda: self.handleStartButton(),
            center=False,
            text="Start Game",
            textSize=15,
            textColor=BLACK,
        )

        self.selected = None
        self.clicked = False

        self.player1 = False
        self.player2 = False
        self.player1Coordinates = " "
        self.player2Coordinates = " "
        self.monsterCount = 0
        self.maxMonster = 10

        self.map = [[' ' for j in range(NUM_BOXES)] for i in range(NUM_BOXES)]

    def handlePlayer(self):
        if self.selected in ("a", "c"):
            (mx, my) = pygame.mouse.get_pos()
            if inBound(mx, my, self.offSetX, self.offSetY, W - self.offSetX, H - self.offSetY):
                (i, j) = ScreenCrdToIdx(mx - self.offSetX, my - self.offSetY, self.boxWidth, self.boxHeight)

                if (self.selected == "a" and not self.player1):
                    self.grid[i][j] = self.selected
                    self.player1Coordinates = (i,j)
                    self.player1 = True
                elif ((self.selected == "a" and self.player1)):
                    (k, l) = self.player1Coordinates
                    print(self.player1Coordinates)
                    self.grid[k][l] = " "
                    self.grid[i][j] = self.selected
                    self.player1Coordinates = (i, j)

                if (self.selected == "c" and not self.player2):
                    self.grid[i][j] = self.selected
                    self.player2Coordinates = (i,j)
                    self.player2 = True
                elif ((self.selected == "c" and self.player2)):
                    (k, l) = self.player2Coordinates
                    print(self.player2Coordinates)
                    self.grid[k][l] = " "
                    self.grid[i][j] = self.selected
                    self.player2Coordinates = (i, j)
        return True


    def handleStartButton(self):
        self.newMap()
        for row in self.map:
            print(row)

    def setSelected(self, elem):
        self.selected = elem

    def start_game(self, file_path):
        self.gameMgr.set_game_window_file_path(file_path)
        game_window = GameWindow(file_path)
        self.gameMgr.setState(GAME_WINDOW, game_window)

    # If the mouse was pressed but the co-ordinates clicked later were not part of the grid
    # Then set selected to None
    def handlePlayerMouse(self):
        if self.selected in ("a", "c") and self.evMgr.mousePressed:
            if not self.handlePlayer():
                self.setSelected(None)


    def handleMonsterMouse(self):
        if self.selected in ("m", "f", "g", "p"):
            (mx, my) = pygame.mouse.get_pos()
            if self.selected and inBound(mx, my, self.offSetX, self.offSetY,
                                         W - self.offSetX, H - self.offSetY):
                if self.calculateMonsterCount() < self.maxMonster and self.evMgr.mousePressed:
                    (i, j) = ScreenCrdToIdx(mx - self.offSetX, my - self.offSetY, self.boxWidth, self.boxHeight)
                    self.grid[i][j] = self.selected
                    self.monsterCount += 1
                    return True
            else:
                return False

    def calculateMonsterCount(self):
        num = 0
        for i in range(NUM_BOXES):
           for j in range(NUM_BOXES):
               if self.grid[i][j] == Monster:
                   num += 1
        return num

    def reset(self):
        self.monsterCount = 0
        self.grid = [[EMPTY for i in range(NUM_BOXES)]
                     for j in range(NUM_BOXES)]

    def getHoveredCell(self):
        (mx, my) = pygame.mouse.get_pos()
        if inBound(mx, my, self.offSetX, self.offSetY, W - self.offSetX, H - self.offSetY):
            (i, j) = ScreenCrdToIdx(mx - self.offSetX, my - self.offSetY, self.boxWidth, self.boxHeight)
            return (i, j)
        else:
            return None

    def continousDraw(self):
        if self.selected and (self.selected not in ("m", "f", "g", "p", "a", "c")):
            hovered_cell = self.getHoveredCell()
            if hovered_cell is not None and self.clicked:
                (i, j) = hovered_cell
                self.grid[i][j] = self.selected

            self.clicked=False




    def handleMousePos(self):
        if self.evMgr.mousePressed:
            if self.selected in ("m", "f", "g", "p"):
                self.handleMonsterMouse()
            if not self.clicked:
                (mx, my) = pygame.mouse.get_pos()
                if inBound(mx, my, self.offSetX, self.offSetY, W - self.offSetX, H - self.offSetY):
                    self.clicked = True
            else:
                self.clicked = False

    # 				     W-self.offSetX, H-self.offSetY):

    # Updates the mouse function after each frame
    # The update function will call the callback function of the buttons
    # backButton goes back to the previous state
    # For box and wall it will set them as the selected element incase the mouse was clicked
    def update(self):

        self.handlePlayerMouse()
        self.backButton.update()
        self.boxButton.update()
        self.wallButton.update()
        self.emptyButton.update()
        self.startButton.update()
        self.resetButton.update()

        mousePressed = pygame.mouse.get_pressed()
        if mousePressed[0]:
            self.evMgr.setMousePressed(True)

        self.handleMousePos()
        self.continousDraw()
        self.handleMonsterMouse()

        self.P1Button.update()
        self.P2Button.update()

        self.baseMButton.update()
        self.ghostMButton.update()
        self.fastMButton.update()
        self.pseudoIntMButton.update()


    def load(self, img):
        return self.imgHandler.load(img, (self.boxWidth, self.boxHeight))

    def newMap(self):
        for i in range(NUM_BOXES):
            for j in range(NUM_BOXES):
                if i in borders or j in borders:
                    self.map[i][j] = "@"
                elif self.grid[i][j] == EMPTY:
                    self.map[i][j] = ' '
                elif self.grid[i][j] == BOX:
                    self.map[i][j] = 'b'
                elif self.grid[i][j] == WALL:
                    self.map[i][j] = '#'
                elif self.grid[i][j] == BASE_MONSTER:
                    self.map[i][j] = "m"
                elif self.grid[i][j] == GHOST_MONSTER:
                    self.map[i][j] = "g"
                elif self.grid[i][j] == FAST_MONSTER:
                    self.map[i][j] = "f"
                elif self.grid[i][j] == PSEUDOINTELLIGENT_MONSTER:
                    self.map[i][j] = "p"

    # def saveToFile(self):
    #	with open()

    def draw(self, display):
        display.fill((110, 161, 100))
        self.backButton.draw(display)
        self.boxButton.draw(display)
        self.wallButton.draw(display)
        self.startButton.draw(display)
        self.resetButton.draw(display)
        self.emptyButton.draw(display)
        self.P1Button.draw(display)
        self.P2Button.draw(display)
        self.baseMButton.draw(display)
        self.ghostMButton.draw(display)
        self.fastMButton.draw(display)
        self.pseudoIntMButton.draw(display)

        # Draws the rectangular lines
        for i in range(NUM_BOXES):
            for j in range(NUM_BOXES):
                x = self.offSetX + j * self.boxWidth;
                y = self.offSetY + i * self.boxHeight;

                if i in borders or j in borders:
                    display.blit(self.load(imgs[WALL]), (x, y))
                else:
                    display.blit(self.load(imgs[self.grid[i][j]]), (x, y))
                    pygame.draw.rect(display, (225, 225, 225), (x, y, self.boxWidth, self.boxHeight), 1)

        # Provides the visual of the selected element when the mouse is moving around
        if self.selected is not None:
            (mx, my) = pygame.mouse.get_pos()
            if inBound(mx, my, self.offSetX, self.offSetY, W - self.offSetX, H - self.offSetY):
                img = self.load(imgs[self.selected])
                img.set_alpha(150)
                display.blit(img, (mx - self.boxWidth / 2, my - self.boxHeight / 2))
                img.set_alpha(255)
