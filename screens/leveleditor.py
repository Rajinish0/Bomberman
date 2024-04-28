import os
import re
from .screen import Screen
from screens.GameWindow import GameWindow
from constants import *
from button import Button
from gameObjects import *
from utils import *
import pygame
from copy import deepcopy
from PIL import Image
import os


'''
TEMPORARY CLASS FOR EXPERIMENTATION PURPOSES.
'''

# For all the images
imgs = {
    BOX: Box.image,
    WALL: Wall.image,
    EMPTY: EmptySpace.image,
    PLAYER1 : "sprites/players/g1.png",
    PLAYER2 : "sprites/players/g2.png",
    BASE_MONSTER : "sprites/monsters/m1b.png",
    GHOST_MONSTER : "sprites/monsters/m1b.png",
    FAST_MONSTER : "sprites/monsters/m1b.png",
    PSEUDOINTELLIGENT_MONSTER : "sprites/monsters/m1b.png"
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
            callBack=lambda: self.go_back()
            ,
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
            80, 200, self.boxWidth, self.boxHeight, img="sprites/players/g1.png",
            callBack=lambda:self.setSelected(PLAYER1),
            center=False
        )

        self.P2Button = Button(
            80, 260, self.boxWidth, self.boxHeight, img="sprites/players/g2.png",
            callBack=lambda:self.setSelected(PLAYER2),
            center=False
        )

        self.baseMButton = Button(
            80, 320, self.boxWidth, self.boxHeight, img="sprites/monsters/m1b.png",
            callBack=lambda: self.setSelected(BASE_MONSTER),
            center=False
        )

        self.ghostMButton = Button(
            80, 380, self.boxWidth, self.boxHeight, img="sprites/monsters/m1b.png",
            callBack=lambda: self.setSelected(GHOST_MONSTER),
            center=False
        )

        self.fastMButton = Button(
            80, 440, self.boxWidth, self.boxHeight, img="sprites/monsters/m1b.png",
            callBack=lambda: self.setSelected(FAST_MONSTER),
            center=False
        )

        self.pseudoIntMButton = Button(
            80, 500, self.boxWidth, self.boxHeight, img="sprites/monsters/m1b.png",
            callBack=lambda: self.setSelected(PSEUDOINTELLIGENT_MONSTER),
            center=False
        )

        self.resetButton = Button(
            x=80, y=550, width=200, height=20,
            callBack=lambda: self.reset(),
            center=False,
            text="Reset Map",
            textSize=15,
            textColor=BLACK,
        )

        self.startButton = Button(
            x=80, y=580, width=200, height=100,
            callBack=lambda: self.handleInitialStart(),
            center=False,
            text="Start Game",
            textSize=15,
            textColor=BLACK,
        )

        self.oKButton = Button(
            420, 300, 30, 30, text="Ok",
            callBack=lambda: self.removePopUp()
        )

        self.nameButton=Button(270+150, 400, 30, 30, text="Enter Name")
        self.startGameButton=Button(270+150, 500, 30, 30, text="Start",
                                    callBack=lambda : self.handleStartButton())
        self.currPressedName=False
        self.selected = None
        self.clicked = False

        self.player1 = False
        self.player2 = False
        self.player1Coordinates = " "
        self.player2Coordinates = " "
        self.monsterCount = 0
        self.maxMonster = 10
        self.directory = 'sprites/levels/'
        self.levels = len(
            [filename for filename in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, filename))])

        self.popUpWindow = False
        self.nameMapWindow=False
        self.map = [[' ' for j in range(NUM_BOXES)] for i in range(NUM_BOXES)]


    def go_back(self):
        self.selected=None
        self.nameMapWindow=False
        self.popUpWindow=False
        self.player1=False
        self.player2=False
        self.reset()
        self.gameMgr.setState(self.gameMgr.getPrevState())


    def removePopUp(self):
        self.popUpWindow = False

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
                    # print(self.player1Coordinates)
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


    def handleInitialStart(self):
        self.selected=None
        if self.player1 and self.player2:
            self.nameMapWindow=True
        else:
            self.popUpWindow=True

    def handleStartButton(self):

        self.nameMapWindow=False
        self.newMap()
        for row in self.map:
            print(row)

        if self.player1 and self.player2:
            background = Image.open("sprites/Solid_white.png")
            background = background.resize((195, 195))
            image = Image.open(imgs[WALL])
            resized_image = image.resize((13, 13))
            width, height = resized_image.size
            y_offset = -height
            for row in self.map:
                y_offset += height
                x_offset = 0
                for elem in row:
                    if elem == "@" or elem == "#":
                        image = Image.open(imgs[WALL])
                        resized_image = image.resize((13, 13))
                        width, height = resized_image.size
                        background.paste(resized_image, (x_offset, y_offset))
                    if elem == " " or elem == "a" or elem == "c":
                        image = Image.open(imgs[EMPTY])
                        resized_image = image.resize((13, 13))
                        width, height = resized_image.size
                        background.paste(resized_image, (x_offset, y_offset))
                    if elem == "b":
                        image = Image.open(imgs[BOX])
                        resized_image = image.resize((13, 13))
                        width, height = resized_image.size
                        background.paste(resized_image, (x_offset, y_offset))
                    x_offset += width


        with open(f'sprites/levels/{self.nameButton.text}.txt', 'w') as f:
            name = f'{self.nameButton.text}.jpg'
            background.save(f'sprites/map_pictures/{name}')
            for row in self.map:
                f.write(''.join(row) + '\n')

        file = f'sprites/levels/{self.nameButton.text}.txt'

        self.main.setState(GAME_WINDOW, GameWindow(file)),
        self.gameMgr.setState(GAME_WINDOW)


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

    def handleEvent(self, event):
        if self.currPressedName:
            text = self.currPressedName.text
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "backspace":
                    text = text[:-1]
                elif pygame.key.name(event.key) == "enter":
                    self.currPressedName = None
                elif re.search("^[a-z]{0,1}[A-Z]{0,1}[0-9]{0,1}-{0,1}_{0,1}$", pygame.key.name(event.key)):
                    text += pygame.key.name(event.key)
            if self.currPressedName:
                self.currPressedName.text = text
    def handleMonsterMouse(self):
        if self.selected in ("m", "f", "g", "p"):
            (mx, my) = pygame.mouse.get_pos()
            if inBound(mx, my, self.offSetX, self.offSetY, W - self.offSetX, H - self.offSetY):
                (i, j) = ScreenCrdToIdx(mx - self.offSetX, my - self.offSetY, self.boxWidth, self.boxHeight)
                # Check if the grid cell is not already occupied by the same monster and count limit not exceeded
                if self.grid[i][j] != self.selected and self.calculateMonsterCount() < self.maxMonster:
                    if self.evMgr.mousePressed:  # Ensure that the mouse button is pressed
                        self.grid[i][j] = self.selected
                        self.monsterCount += 1
                        return True
            return False

    def calculateMonsterCount(self):
        count = 0
        for row in self.grid:
            count += row.count(BASE_MONSTER) + row.count(GHOST_MONSTER) + row.count(FAST_MONSTER) + row.count(
                PSEUDOINTELLIGENT_MONSTER)
        return count

    def reset(self):
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
                if self.grid[i][j]=="a":
                    self.player1=False
                if self.grid[i][j]=="c":
                    self.player2=False
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
        self.oKButton.update()
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
        if self.nameMapWindow:
            self.nameButton.update()

            if self.nameButton.pressed:
                self.currPressedName=self.nameButton
            self.startGameButton.update()

        self.levels = len(
            [filename for filename in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, filename))])

    def load(self, img):
        return self.imgHandler.load(img, (self.boxWidth, self.boxHeight))

    def newMap(self):
        print("Here")
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
                elif self.grid[i][j] == PLAYER1:
                    self.map[i][j] = "a"
                elif self.grid[i][j] == PLAYER2:
                    self.map[i][j] = "c"

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
                x = self.offSetX + j * self.boxWidth
                y = self.offSetY + i * self.boxHeight

                display.blit(self.load(imgs[EMPTY]), (x,y))

                if i in borders or j in borders:
                    display.blit(self.load(imgs[WALL]), (x, y))
                else:
                    display.blit(self.load(imgs[self.grid[i][j]]), (x, y))
                    pygame.draw.rect(display, (225, 225, 225), (x, y, self.boxWidth, self.boxHeight), 1)

        if self.selected is not None:
            (mx, my) = pygame.mouse.get_pos()
            if inBound(mx, my, self.offSetX, self.offSetY, W - self.offSetX, H - self.offSetY):
                img = self.load(imgs[self.selected])
                img.set_alpha(150)
                display.blit(img, (mx - self.boxWidth / 2, my - self.boxHeight / 2))
                img.set_alpha(255)

        if self.nameMapWindow:
            x = 270
            y = 220
            width = 300
            height = 300
            font_size = 20
            text_color = (255, 255, 255)
            bg_color = (255, 0, 0)

            rect = pygame.Rect(x, y, width, height)
            pygame.draw.rect(display, bg_color, rect)
            font = pygame.font.SysFont(None, font_size)
            text_surface = font.render("Name Window", True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            display.blit(text_surface, text_rect)
            self.nameButton.draw(display)
            self.startGameButton.draw(display)

        if self.popUpWindow:
            x = 270
            y = 220
            width = 300
            height = 100
            font_size = 20
            text_color = (255, 255, 255)
            bg_color = (255, 0, 0)

            rect = pygame.Rect(x, y, width, height)
            pygame.draw.rect(display, bg_color, rect)
            font = pygame.font.SysFont(None, font_size)
            text_surface = font.render("2 Players Should Be Placed", True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            display.blit(text_surface, text_rect)
            self.oKButton.draw(display)
