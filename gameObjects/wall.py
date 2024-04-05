from gameObjects.gameObject import GameObject
import pygame

class Wall(GameObject):
    image = "sprites/gameobjects/wall.JPEG"
    def __init__(self, position, width, height):
        super().__init__(position)
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
    def draw(self, display):
        display.blit(self.image, (self.position.x, self.position.y))