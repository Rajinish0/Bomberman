from screens.screen import Screen
from constants import *
from button import Button
import pygame
from fileReading import GridReader
from gameObjects.wall import Wall
from gameObjects.box import Box
from gameObjects.emptySpace import EmptySpace
from point import Point

class GameWindow(Screen):
    def __init__(self, file_path=None):
        self.file_path = file_path
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

        if file_path is not None:
            reader = GridReader(file_path)
            reader.read_grid()
            self.grid = reader.get_grid()

    def update(self):
        self.backButton.update()

    def draw(self, display):
        display.fill((239, 233, 222))
        self.backButton.draw(display)

        for i in range(NUM_BOXES):
            for j in range(NUM_BOXES):
                #pygame.draw.rect(display, BLACK, (
                #98 + j * self.boxWidth, 70 + i * self.boxHeight, self.boxWidth, self.boxHeight), 1)
                # Calculate position based on grid coordinates
                pos_x = 98 + j * self.boxWidth
                pos_y = 70 + i * self.boxHeight
                position = Point(pos_x, pos_y)

                # Check what's on the grid and initialize the corresponding object
                if self.grid[i][j] == 'b':
                    element = Box(position, 1, self.boxWidth, self.boxHeight)
                elif self.grid[i][j] == '#':
                    element = Wall(position, 1, self.boxWidth, self.boxHeight)
                else:
                    element = EmptySpace(position, 1, self.boxWidth, self.boxHeight)

                # Draw the element (assuming these objects have a draw method)
                element.draw(display)
