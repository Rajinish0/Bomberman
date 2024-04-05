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
            callBack=lambda: self.gameMgr.setState(MAP_WINDOW)
        )

        if file_path is not None:
            reader = GridReader(file_path)
            reader.read_grid()
            self.grid = reader.get_grid()

    def update(self):
        self.backButton.update()

    def draw(self, display):
        display.fill((110, 161, 100))

        # background_image = pygame.image.load('sprites/backgrnd.png')
        # scaled_image = pygame.transform.scale(background_image, (W, H))
        # alpha_value_bg = 260
        # scaled_image.set_alpha(alpha_value_bg)
        # display.blit(scaled_image, (0, 0))

        for i in range(NUM_BOXES):
            for j in range(NUM_BOXES):
                pos_x = 98 + j * self.boxWidth
                pos_y = 70 + i * self.boxHeight
                position = Point(pos_x, pos_y)
                if self.grid[i][j] == 'b':
                    element = Box(position, 1, self.boxWidth, self.boxHeight)
                elif self.grid[i][j] == '#':
                    element = Wall(position, 1, self.boxWidth, self.boxHeight)
                else:
                    element = EmptySpace(position, 1, self.boxWidth, self.boxHeight)
                element.draw(display)

        self.backButton.draw(display)

