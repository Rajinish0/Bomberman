from .screen import Screen
from constants import *
from button import Button
import pygame

class GameWindow(Screen):
    def __init__(self):
        self.offSetX = 200
        self.offSetY = 0
        self.boxWidth = (800 - self.offSetX) // NUM_BOXES
        self.boxHeight = (520 - self.offSetY) // NUM_BOXES
        self.grid = [[EMPTY for i in range(NUM_BOXES)]
                     for j in range(NUM_BOXES)]
        self.backButton = Button(
            30, 30, 30, 30, text="Back",
            callBack=lambda: self.gameMgr.setState(
                self.gameMgr.getPrevState()
            )
        )

    def update(self):
        self.backButton.update()

    def draw(self, display):
        display.fill((239, 233, 222))
        self.backButton.draw(display)

        for i in range(NUM_BOXES):
            for j in range(NUM_BOXES):
                pygame.draw.rect(display, BLACK, (
                98 + j * self.boxWidth, 70 + i * self.boxHeight, self.boxWidth, self.boxHeight), 1)
