from gameObjects.gameObject import GameObject
import pygame

class Wall(GameObject):
    image = "sprites/gameobjects/wall.JPEG"
    def __init__(self, position, width, height):
        super().__init__(position, width, height)
        self.image = self.imageHandler.load(self.image, (self.width, self.height))
    def draw(self, display):
        display.blit(self.image, (self.position.x, self.position.y))