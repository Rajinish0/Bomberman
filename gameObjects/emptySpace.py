from gameObjects.gameObject import GameObject
import pygame

class EmptySpace(GameObject):
    image = "sprites/gameobjects/grass.jpg"
    def __init__(self, position,width, height):
        super().__init__(position, width, height)
        self.image = self.imgHandler.load(EmptySpace.image, (width, height))



