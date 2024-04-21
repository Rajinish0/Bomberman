from screens.screen import Screen
from constants import *
from button import Button
import pygame, os
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
        self.boxWidth = (800 - self.offSetX) // NUM_BOXES
        self.boxHeight = (520 - self.offSetY) // NUM_BOXES
        self.level = GameLevel(file_path,self.boxWidth,self.boxHeight)
        self.gamesurface = pygame.Surface((800-self.offSetX, 520-self.offSetY), pygame.SRCALPHA)
        self.infosurface = pygame.Surface((800-self.offSetX, (H-520+70)) )
        self.pl1Image = self.imgHandler.load( os.path.join(IMG_PATH, 'players', 'g1.png'), (50, 70) )
        self.pl2Image = self.imgHandler.load( os.path.join(IMG_PATH, 'players', 'g2.png'), (50, 70) )


        self.backButton = Button(
            30, 30, 30, 30, text="Back",
            callBack=lambda: self.gameMgr.setState(MAP_WINDOW)
        )





    def update(self):
        self.backButton.update()
        self.level.update()



    def draw(self, display):
        display.fill((110, 161, 100))
        self.gamesurface.fill((110, 161, 100))
        self.infosurface.fill((110, 161, 100))
        self.infosurface.blit(self.pl1Image, (0, 0))
        self.infosurface.blit(self.pl2Image, ((800-self.offSetX)-50, 0))
        self.backButton.draw(display)
        self.level.draw(self.gamesurface)
        display.blit(self.infosurface, (98, 0))
        display.blit(self.gamesurface, (98, 70))

