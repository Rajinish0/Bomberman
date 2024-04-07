from gameObjects.gameObject import GameObject
import pygame

class Box(GameObject):
    image = "sprites/gameobjects/boxImg.JPEG"
    def __init__(self, position, width, height):
        super().__init__(position, width, height)
        self.hasPowerup = False
        self.powerUp = None
        self.image = self.imageHandler.load(self.image, (self.width, self.height))

    def update(self, dt):
        pass

    def draw(self, display):
        display.blit(self.image, (self.position.x, self.position.y))

    def blowUp(self):
        pass

    def generatePowerUp(self):
        pass