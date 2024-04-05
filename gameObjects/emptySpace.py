from gameObjects.gameObject import GameObject
import pygame

class EmptySpace(GameObject):
    def __init__(self, position, level, width, height):
        super().__init__("empty", position, "sprites/grass.jpg", level)
        self.image = pygame.image.load("sprites/grass.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
    def draw(self, display):
        display.blit(self.image, (self.position.x, self.position.y))