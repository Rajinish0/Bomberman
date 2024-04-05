from gameObjects.gameObject import GameObject
import pygame

class Wall(GameObject):
    def __init__(self, position, level, width, height):
        super().__init__("wall", position, "sprites/gameobjects/wall.JPEG", level)
        self.image = pygame.image.load("sprites/gameobjects/wall.JPEG").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
    def draw(self, display):
        display.blit(self.image, (self.position.x, self.position.y))