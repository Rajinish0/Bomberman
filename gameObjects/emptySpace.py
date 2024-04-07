from gameObjects.gameObject import GameObject
import pygame
from handlers import ImageHandler

class EmptySpace(GameObject):
    image = "sprites/gameobjects/grass.jpg"
    def __init__(self, position,width, height):
        super().__init__(position, width, height)
        self.image = self.imageHandler.load(self.image, (self.width, self.height))

    def draw(self, display):
        display.blit(self.image, (self.position.x, self.position.y))

    def bomb_explode(self, display):
        display.blit("sprites/orange.png", (self.position.x, self.position.y))