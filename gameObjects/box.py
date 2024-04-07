from gameObjects.gameObject import GameObject
import pygame

class Box(GameObject):
    image = "sprites/gameobjects/boxImg.JPEG"
    def __init__(self, position, width, height):
        super().__init__(position)
        self.hasPowerup = False
        self.powerUp = None
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    def update(self, dt):
        pass

    def draw(self, display):
        display.blit(self.image, (self.position.x, self.position.y))

    def blowUp(self):
        pass

    def generatePowerUp(self):
        pass