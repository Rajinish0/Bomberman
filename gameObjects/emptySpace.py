from gameObjects.gameObject import GameObject
import pygame

class EmptySpace(GameObject):
    def __init__(self, position, level, width, height):
        super().__init__("empty", position, "sprites/emptySpace.png", level)
        self.image = pygame.image.load("sprites/emptySpace.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
    def draw(self, display):
        display.blit(self.image, (self.position.x, self.position.y))

    def bomb_explode(self, display):
        display.blit("sprites/orange.png", (self.position.x, self.position.y))