from screens.screen import Screen
from constants import *
from button import Button
import pygame
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
        self.gamesurface = pygame.Surface((800-self.offSetX, 520-self.offSetY))

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
        self.backButton.draw(display)
        self.level.draw(self.gamesurface)
        display.blit(self.gamesurface, (98, 70))


