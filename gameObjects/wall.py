from gameObjects.gameObject import GameObject
import pygame

class Wall(GameObject):
    image = "sprites/gameobjects/wall.JPEG"
    def __init__(self, position, width, height):
        super().__init__(position, width, height)
        self.image = self.imgHandler.load(Wall.image, (width, height))

class BorderWall(Wall):
    def __init__(self, position, width, height):
        super().__init__(position, width, height)
