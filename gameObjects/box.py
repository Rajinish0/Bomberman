from gameObjects.gameObject import GameObject
import pygame

class Box(GameObject):
    def __init__(self, position, level, width, height):
        super().__init__("box", position, "sprites/gameobjects/boxImg.JPEG", level)
        self.hasPowerup = False
        self.powerUp = None
        self.image = pygame.image.load("sprites/gameobjects/boxImg.JPEG").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    def update(self, dt):
        pass

    def draw(self, display):
        display.blit(self.image, (self.position.x, self.position.y))

    def blowUp(self):
        pass

    def generatePowerUp(self):
        pass