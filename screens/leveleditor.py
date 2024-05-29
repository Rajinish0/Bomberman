import os
import re

from PIL import Image


from .screen import Screen
from screens.GameWindow import GameWindow
from constants import *
from button import Button
from gameObjects import *
from utils import *
import pygame
from copy import deepcopy

import os


'''
TEMPORARY CLASS FOR EXPERIMENTATION PURPOSES.
'''

# For all the images
imgs = {
    BOX: Box.image,
    WALL: Wall.image,
    EMPTY: "UI/grass_tile2.png",
    PLAYER1 : "UI/p2.png",
    PLAYER2 : "UI/p1.png",
    BASE_MONSTER : "UI/monster_new_1.png",
    GHOST_MONSTER : "UI/monster_new_2.png",
    FAST_MONSTER : "UI/monster_new_3.png",
    PSEUDOINTELLIGENT_MONSTER : "UI/monster_new_4.png"
}

# The surrounding borders
borders = [0, NUM_BOXES - 1]


# Checks whether the mouse click was within a rectangular grid or not
def inBound(x, y, lx, ly, w, h):
    return (lx < x < lx + w and
            ly < y < ly + h)


# Converts the co-ordinates of the mouse click to indices of the grid
def ScreenCrdToIdx(x, y, width, height):
    return (y // height, x // width)

class LevelEditor(Screen):

    def __init__(self):
        self.offSetX = 180
        self.offSetY = 40
        self.boxWidth = ((W - self.offSetX) // NUM_BOXES) - 13
        self.boxHeight = ((H - self.offSetY) // NUM_BOXES) - 5

        self.grid = [[EMPTY for i in range(NUM_BOXES)]
                     for j in range(NUM_BOXES)]


        self.backButton = Button(
            85, 475, 30, 30,
            callBack=lambda: self.go_back(),
            img = "UI/wizard2.png",
            center=False
        )

        self.resetButton = Button(
            x=135, y=475, width=30, height=30,
            callBack=lambda: self.reset(),
            center=False,
            img = "UI/delete.png",
            textSize=15,
            textColor=BLACK,
        )

        self.ExitButton = Button(920, 70, 30, 30, textColor=BLACK,
                                 callBack=lambda: pygame.quit(), img='UI/exit.png', textSize=25)

        self.background_image = pygame.image.load('UI/holder.png')
        self.background_image = pygame.transform.scale(self.background_image, (80, 70))
        self.data_frame_image = pygame.image.load('UI/info_box.png')
        self.data_frame_image = pygame.transform.scale(self.data_frame_image, (W / 4-10, H / 4-30))
        #self.data_frame_image=pygame.transform.rotate(self.data_frame_image,180)
        self.data_frame_image=pygame.transform.flip(self.data_frame_image,False,True)
        self.name_fame_image=pygame.image.load('UI/button_clear.png')
        self.name_fame_image=pygame.transform.scale(self.name_fame_image,(W/3,H/3))
        self.boxButton = Button(
            820, 280, self.boxWidth, self.boxHeight, img=imgs[BOX],
            callBack=lambda: self.setSelected(BOX),
            center=False
        )

        self.P1Button = Button(
            820, 460, self.boxWidth, self.boxHeight, img="UI/p1.png",
            callBack=lambda:self.setSelected(PLAYER1),
            center=False
        )

        self.P2Button = Button(
            820, 370, self.boxWidth, self.boxHeight, img="UI/p2.png",
            callBack=lambda:self.setSelected(PLAYER2),
            center=False
        )

        self.wallButton = Button(
            820, 110, self.boxWidth, self.boxHeight, img=imgs[WALL],
            callBack=lambda: self.setSelected(WALL),
            center=False
        )

        self.emptyButton = Button(
            820, 190, self.boxWidth, self.boxHeight, img=imgs[EMPTY],
            callBack=lambda: self.setSelected(EMPTY),
            center=False
        )

        self.baseMButton = Button(
            110, 190, self.boxWidth, self.boxHeight, img=imgs[BASE_MONSTER],
            callBack=lambda: self.setSelected(BASE_MONSTER),
            center=False
        )

        self.ghostMButton = Button(
            110, 280, self.boxWidth, self.boxHeight, img=imgs[GHOST_MONSTER],
            callBack=lambda: self.setSelected(GHOST_MONSTER),
            center=False
        )

        self.fastMButton = Button(
            110, 370, self.boxWidth, self.boxHeight, img=imgs[FAST_MONSTER],
            callBack=lambda: self.setSelected(FAST_MONSTER),
            center=False
        )

        self.pseudoIntMButton = Button(
            110, 110, self.boxWidth, self.boxHeight, img=imgs[PSEUDOINTELLIGENT_MONSTER],
            callBack=lambda: self.setSelected(PSEUDOINTELLIGENT_MONSTER),
            center=False
        )

        self.startButton = Button(
            W / 2 - 20, 530, 180, 40, text="Start", color=BLACK, textColor=BLACK,
            callBack=lambda: (self.handleInitialStart()), img='UI/button.png', textSize=10
        )

        self.oKButton = Button(
            W/2+70+W/8-5,530-H/4+30+80, 50, 25, text="Ok", img='UI/button_clear.png',color=BLACK, textColor=BLACK,textSize=12,
            callBack=lambda: self.removePopUp()
        )
        self.frame_image = pygame.image.load('UI/frame.png')
        self.frame_image = pygame.transform.scale(self.frame_image, (60, 80))

        self.nameButton=Button(W/2,H/2-H/6+95, 140, 40, text="Enter Name",textColor=BLACK,color=WHITE,drawRect=True,center=True,textSize=10)
        self.startGameButton=Button(W/2+75,H/2-H/6+140, 50, 25, text="Start",textColor=BLACK,textSize=15,
                                    callBack=lambda : self.handleStartButton())
        self.backGameButton=Button(W/2-75,H/2-H/6+140, 50, 25, text="Back",textColor=BLACK,textSize=15,
                                    callBack=lambda : self.handleBackButton())
        self.currPressedName=False
        self.selected = None
        self.clicked = False
        self.caps=False
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
            (i, j) = ScreenCrdToIdx(mx - self.offSetX, my - self.offSetY, self.boxWidth, self.boxHeight)
            if self.inBound(mx, my) and (i not in borders and j not in borders):

                if (self.selected == "a" and not self.player1):
                    self.grid[i][j] = self.selected
                    self.player1Coordinates = (i,j)
                    self.player1 = True
                    self.player2 = (self.player2 and self.player2Coordinates != self.player1Coordinates)
                elif ((self.selected == "a" and self.player1)):
                    (k, l) = self.player1Coordinates
                    # print(self.player1Coordinates)
                    self.grid[k][l] = " "
                    self.grid[i][j] = self.selected
                    self.player1Coordinates = (i, j)
                    self.player2 = (self.player2 and self.player2Coordinates != self.player1Coordinates)

                if (self.selected == "c" and not self.player2):
                    self.grid[i][j] = self.selected
                    self.player2Coordinates = (i,j)
                    self.player2 = True
                    self.player1 = (self.player1 and self.player1Coordinates != self.player2Coordinates)

                elif ((self.selected == "c" and self.player2)):
                    (k, l) = self.player2Coordinates
                    print(self.player2Coordinates)
                    self.grid[k][l] = " "
                    self.grid[i][j] = self.selected
                    self.player2Coordinates = (i, j)
                    self.player1 = (self.player1 and self.player1Coordinates != self.player2Coordinates)
        return True


    def handleInitialStart(self):
        self.selected=None
        if self.player1 and self.player2:
            self.nameMapSurface = pygame.Surface((300, 150))
            self.nameMapWindow=True
        else:
            self.popUpWindow=True

    def handleBackButton(self):
        self.nameMapWindow=False
    def handleStartButton(self):

        self.nameMapWindow=False
        self.newMap()
        for row in self.map:
            print(row)

        if self.player1 and self.player2:
            background = Image.open("UI/map_frame.png")
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

                    if elem == " " or elem == "a" or elem == "c" or elem == "m" or elem == "f" or elem == "p" or elem == "g":

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

        cnt=1
        while(os.path.exists(os.path.join(self.directory,self.nameButton.text+".txt"))):
            self.nameButton.text+=str(cnt)
            cnt+=1
        with open(f'sprites/levels/{self.nameButton.text}.txt', 'w') as f:
            name = f'{self.nameButton.text}.png'
            background.save(f'sprites/map_pictures/{name}')
            for row in self.map:
                f.write(''.join(row) + '\n')

        file = f'sprites/levels/{self.nameButton.text}.txt'
        self.reset()
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
                if pygame.key.name(event.key) == "left shift":
                    self.caps=True
                if pygame.key.name(event.key) == "backspace":
                    text = text[:-1]
                elif pygame.key.name(event.key) == "enter":
                    self.currPressedName = None
                elif pygame.key.name(event.key)=="space":
                    text +=" "
                elif re.search("^[a-z]{0,1}[A-Z]{0,1}[0-9]{0,1}-{0,1}_{0,1}$", pygame.key.name(event.key)):
                    if self.caps:
                        text += pygame.key.name(event.key).upper()
                    else:
                        text += pygame.key.name(event.key)

            if self.currPressedName:
                self.currPressedName.text = text
        if event.type==pygame.KEYUP:
            if pygame.key.name(event.key) == "left shift":
                self.caps = False
    def handleMonsterMouse(self):
        if self.selected in ("m", "f", "g", "p"):
            (mx, my) = pygame.mouse.get_pos()
            (i, j) = ScreenCrdToIdx(mx - self.offSetX, my - self.offSetY, self.boxWidth, self.boxHeight)
            if self.inBound(mx, my) and (i not in borders and j not in borders):
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
        self.player1 = False
        self.player2 = False
        self.player1Coordinates = " "
        self.player2Coordinates = " "
        self.monsterCount = 0

    def inBound(self, x, y):
        return inBound(x, y, self.offSetX, self.offSetY, self.boxWidth*NUM_BOXES, self.boxHeight*NUM_BOXES)

    def getHoveredCell(self):
        (mx, my) = pygame.mouse.get_pos()
        if self.inBound(mx, my):
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
                if self.inBound(mx, my):
                    self.clicked = True
            else:
                self.clicked = False

    def update(self):
        self.ExitButton.update()
        if self.nameMapWindow:
            self.startGameButton.update()
            self.backGameButton.update()
            self.nameButton.update()

            if self.nameButton.pressed:
                self.currPressedName=self.nameButton
        else:
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



        #self.levels = len(
        #   [filename for filename in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, filename))])

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

        display.fill((114, 125, 104))

        display.blit(self.background_image, (90, 90))
        display.blit(self.background_image, (90, 170))
        display.blit(self.background_image, (90, 260))
        display.blit(self.background_image, (90, 350))
        display.blit(self.background_image, (800, 90))
        display.blit(self.background_image, (800, 170))
        display.blit(self.background_image, (800, 260))
        display.blit(self.background_image, (800, 350))
        display.blit(self.background_image, (800, 440))

        x_increment = 50
        frame_rotated_image = pygame.transform.rotate(self.frame_image, +90)
        for i in range(20):
            display.blit(frame_rotated_image, (30 + i * x_increment, -15))

        frame_rotated_image = pygame.transform.rotate(self.frame_image, -90)
        for i in range(20):
            display.blit(frame_rotated_image, (35 + i * x_increment, 550))

        y_increment = 50
        frame_rotated_image = pygame.transform.rotate(self.frame_image, -180)
        for i in range(12):
            display.blit(frame_rotated_image, (-15, -15 + i * y_increment))

        for i in range(12):
            display.blit(self.frame_image, (950, -15 + i * y_increment))

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
        self.ExitButton.draw(display)

        # Draws the rectangular lines
        for i in range(NUM_BOXES):
            for j in range(NUM_BOXES):
                x = self.offSetX + j * self.boxWidth
                y = self.offSetY + i * self.boxHeight

                if i not in borders and j not in borders:
                    display.blit(self.load(imgs[EMPTY]), (x, y))
                    display.blit(self.load(imgs[self.grid[i][j]]), (x, y))
                    pygame.draw.rect(display, BLACK, (x, y, self.boxWidth, self.boxHeight), 1)

        if self.selected is not None:
            (mx, my) = pygame.mouse.get_pos()
            if self.inBound(mx, my):
                img = self.load(imgs[self.selected])
                img.set_alpha(150)
                display.blit(img, (mx - self.boxWidth / 2, my - self.boxHeight / 2))
                img.set_alpha(255)

        if self.nameMapWindow:
            # pygame.draw.rect(self.nameMapSurface, (238, 238, 238, 240), self.nameMapSurface.get_rect())
            # display.blit(self.nameMapSurface, (270, 220))
            display.blit(self.name_fame_image, (W / 2 -W/6, H/2-H/6))
            drawText(display,"Name the map",W/2,H/2-H/6+50,size=20,color=BLACK)
            self.nameButton.draw(display,Border=True,BorderWidth=1)
            self.startGameButton.draw(display)
            self.backGameButton.draw(display)

        if self.popUpWindow:
            x = 270
            y = 220
            width = 300
            height = 100
            font_size = 20
            text_color = (255, 255, 255)
            bg_color = (255, 0, 0)

            # rect = pygame.Rect(x, y, width, height)
            # pygame.draw.rect(display, bg_color, rect)

            display.blit(self.data_frame_image, (W / 2 +63,530-H/4+30))

            drawText(display,"2 Players Should",W/2+70+W/8-5,530-H/4+30+30,size=11,color=BLACK)
            drawText(display,"Be Placed",W/2+70+W/8-5,530-H/4+30+30+20,size=11,color=BLACK)

            # font = pygame.font.SysFont(None, font_size)
            # text_surface = font.render("2 Players Should Be Placed", True, text_color)
            # text_rect = text_surface.get_rect(center=rect.center)
            # display.blit(text_surface, text_rect)
            self.oKButton.draw(display)
