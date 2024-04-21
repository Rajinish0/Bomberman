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
        self.infosurface = pygame.Surface((self.gameWidth, (H-self.gameHeight+70)) )
        self.pl1Image = self.imgHandler.load( os.path.join(IMG_PATH, 'players', 'g1.png'), (50, 70) )
        self.pl2Image = self.imgHandler.load( os.path.join(IMG_PATH, 'players', 'g2.png'), (50, 70) )


        self.backButton = Button(
            30, 30, 30, 30, text="Back",
            callBack=lambda: self.gameMgr.setState(MAP_WINDOW)
        )

        self.nextButton=Button(
            W/2,H/2+40,30,30,text="Next Round",
            callBack=lambda :(self.level.nextRound(),
                              resetCursor())
        )
        self.menuButton=Button(
            W / 2, H / 2 + 40, 30, 30, text="Go to Menu",
            callBack=lambda: self.gameMgr.setState(MAIN_WINDOW)
        )
        self.restartButton=Button(
            W / 2, H / 2 + 80, 30, 30, text="Restart Game",
            callBack=lambda: (self.level.restart(),
                              resetCursor())
        )





    def update(self):
        self.backButton.update()
        self.level.update()
        if self.level.finished:
            self.menuButton.update()
            self.restartButton.update()
        elif self.level.gameEnd:
            self.nextButton.update()



    def draw(self, display):
        display.fill((110, 161, 100))
        self.gamesurface.fill((110, 161, 100))
        self.infosurface.fill((110, 161, 100))
        self.infosurface.blit(self.pl1Image, (0, 0))
        self.infosurface.blit(self.pl2Image, ((self.gameWidth)-50, 0))
        self.backButton.draw(display)

        drawText(self.infosurface,PLAYER1_NAME,55,10,size=18,color=WHITE,center=False)
        drawText(self.infosurface, self.level.player1Wins, 55, 30, size=18, color=WHITE, center=False)
        drawText(self.infosurface, PLAYER2_NAME, (self.gameWidth)-55, 10, size=18, color=WHITE, center=False, right=True)
        drawText(self.infosurface, self.level.player2Wins, (self.gameWidth)-55, 30, size=18, color=WHITE, center=False,right=True)
        if self.level.finished:
            text=self.level.players[0].name+ " has won the game!!!"
            display.blit(self.infosurface, (98, 0))
            drawText(display, text, W / 2, H / 2)
            self.menuButton.draw(display)
            self.restartButton.draw(display)
        elif self.level.gameEnd:
            text = "No one won this round!!!"
            if self.level.players:
                text = self.level.players[0].name+" has won the round!!!"

            display.blit(self.infosurface, (98, 0))
            drawText(display ,text,W/2,H/2)

            self.nextButton.draw(display)
        else:
            self.level.draw(self.gamesurface)
            display.blit(self.infosurface, (98, 0))
            display.blit(self.gamesurface, (98, 70))








