from .screen import Screen
from constants import *
from button import Button
import pygame
import os

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
        self.buttons = []
        for i in range(NUM_BOXES):
            row = []
            for j in range(NUM_BOXES):
                x = 98 + j * self.boxWidth
                y = 70 + i * self.boxHeight
                button = Button(x, y, 10, 10, img = os.path.join (IMG_PATH, 'start.png'))
                row.append(button)
            self.buttons.append(row)

    def update(self):
        self.backButton.update()

        for row in self.buttons:
            for button in row:
                button.update()

    def draw(self, display):
        display.fill((239, 233, 222))
        self.backButton.draw(display)

        for row in self.buttons:
            for button in row:
                button.draw(display)


