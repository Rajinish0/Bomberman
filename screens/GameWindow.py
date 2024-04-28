import math
import pickle

import gamelevel
from screens.screen import Screen
from constants import *
from button import Button
import pygame, os
from utils import *
from fileReading import GridReader
from gameObjects.wall import Wall
from gameObjects.box import Box
from gameObjects.emptySpace import EmptySpace
from gameObjects.Player import Player
from point import Point
from gamelevel import GameLevel


class GameWindow(Screen):
    def __init__(self, file_path=None):


        self.file_path = file_path
        self.offSetX = 200
        self.offSetY = 0
        self.gameWidth=800-self.offSetX
        self.gameHeight=520-self.offSetY
        self.boxWidth = (self.gameWidth) // NUM_BOXES
        self.boxHeight = (520 - self.offSetY) // NUM_BOXES
        self.level = GameLevel(file_path,self.boxWidth,self.boxHeight)
        self.gamesurface = pygame.Surface((self.gameWidth, self.gameHeight), pygame.SRCALPHA)
        self.infosurface = pygame.Surface((self.gameWidth, (H-self.gameHeight+70)))
        self.pWidth, self.pHeight = int(self.gameWidth*0.75), self.gameHeight//2
        self.popUpWindow = pygame.Surface(  (self.pWidth, self.pHeight), pygame.SRCALPHA )
        self.pl1Image = self.imgHandler.load( os.path.join(IMG_PATH, 'players', 'g1.png'), (50, 70) )
        self.pl2Image = self.imgHandler.load( os.path.join(IMG_PATH, 'players', 'g2.png'), (50, 70) )
        self.timer=5
        self.timeList=[3,2,1]





       # self.battleTimer = 14 * 14

        self.backButton = Button(
            30, 30, 30, 30, text="Back",
            callBack=lambda: self.gameMgr.setState(MAP_WINDOW)
        )

        # self.nextButton=Button(
        #     W/2,H/2+40,30,30,text="Next Round",
        #     callBack=lambda :(self.level.nextRound(),
        #                       resetCursor())
        # )
        self.menuButton=Button(
            W / 2, H / 2 + 40, 30, 30, text="Go to Menu",
            callBack=lambda: self.gameMgr.setState(MAIN_WINDOW),
            textColor = BLACK
        )
        self.restartButton=Button(
            W / 2, H / 2 + 80, 30, 30, text="Restart Game",
            callBack=lambda: (self.level.restart(),
                              resetCursor()),
            textColor = BLACK
        )


    def update(self):
        self.backButton.update()
        self.level.update()

        if self.level.finished:
            self.menuButton.update()
            self.restartButton.update()
        elif self.level.gameEnd:
            if self.timer>0:
                self.timer-=1/FPS
            else:
                self.level.nextRound()
                self.timer = 5
                self.level.nextRound()

    def getTimer(self):
        if self.level.brTimer<=0:
            return ("00:00",RED)
        else:
            min=str(math.floor(math.ceil(self.level.brTimer)/60)).zfill(2)
            sec=str(math.ceil(self.level.brTimer)%60).zfill(2)
            text=min+":"+sec
            if self.level.brTimer<4:
                # print(self.level.brTimer)
                return (text,RED)
            else:
                return (text,WHITE)

    def getBattleTimer(self):
        if self.level.battleTimer<=0:
            return ("00:00",RED)
        min=str(math.floor(math.ceil(self.level.battleTimer)/60)).zfill(2)
        sec=str(math.ceil(self.level.battleTimer)%60).zfill(2)
        text=min+":"+sec
        return (text,RED)


    def draw(self, display):
        display.fill((110, 161, 100))
        self.gamesurface.fill((110, 161, 100))
        self.infosurface.fill((110, 161, 100))
        self.infosurface.blit(self.pl1Image, (0, 0))
        self.infosurface.blit(self.pl2Image, ((self.gameWidth)-50, 0))
        self.backButton.draw(display)
        timer = self.getTimer()
        drawText(self.infosurface,timer[0],self.gameWidth/2,30,size=50,color=timer[1],center=True)
        # if not self.level.brTimer <= 0:
        #     timer=self.getTimer()
        #     drawText(self.infosurface,timer[0],self.gameWidth/2,30,size=50,color=timer[1],center=True)
        # else:
        #     timer = self.getBattleTimer()
        #     drawText(self.infosurface, timer[0], self.gameWidth / 2, 30, size=50, color=timer[1], center=True)

        drawText(self.infosurface,self.level.pl1Name,55,10,size=18,color=WHITE,center=False)
        drawText(self.infosurface, self.level.player1Wins, 55, 30, size=18, color=WHITE, center=False)
        drawText(self.infosurface, self.level.pl2Name, (self.gameWidth)-55, 10, size=18, color=WHITE, center=False, right=True)
        drawText(self.infosurface, self.level.player2Wins, (self.gameWidth)-55, 30, size=18, color=WHITE, center=False,right=True)
        if self.level.finished:
            self.timer=5
            pygame.draw.rect(self.popUpWindow, (238, 238, 238, 240), self.popUpWindow.get_rect(), border_radius=8)
            text=self.level.players[0].name+ " has won the game!!!"
            self.level.draw(self.gamesurface)
            display.blit(self.infosurface, (98, 0))
            display.blit(self.gamesurface, (98, 70))
            display.blit(self.popUpWindow, (W/2 - self.pWidth/2, H/2 - self.pHeight/2) )
            drawText(display, text, W / 2, H / 2 - self.pHeight/2 + 30, color=BLACK)
            self.menuButton.draw(display)
            self.restartButton.draw(display)

        elif self.level.gameEnd:
            self.level.draw(self.gamesurface)

            text = "No one won this round!!!"
            if self.level.players:
                text = self.level.players[0].name+" has won the round!!!"

            display.blit(self.infosurface, (98, 0))
            display.blit(self.gamesurface, (98, 70))
            drawText(display,text,W/2,H/2,color=WHITE,size=30)
            drawText(display,math.ceil(self.timer), W / 2, H / 2 +100,color=WHITE,size=50)


            # self.nextButton.draw(display)
        else:
            self.level.draw(self.gamesurface)
            display.blit(self.infosurface, (98, 0))
            display.blit(self.gamesurface, (98, 70))











