from gameObjects.gameObject import GameObject
import pygame

class EmptySpace(GameObject):
    image = "sprites/gameobjects/grass.jpg"
    def __init__(self, position,width, height):
        super().__init__(position)
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
    def draw(self, display):
        display.blit(self.image, (self.position.x, self.position.y))

    def bomb_explode(self, display):
        display.blit("sprites/orange.png", (self.position.x, self.position.y))
