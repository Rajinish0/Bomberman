from gameObjects.gameObject import GameObject
import pygame
from .powerup import *
import random

from point import Point


class Box(GameObject):
    image = "sprites/gameobjects/boxImg.JPEG"
    def __init__(self, position, width, height):
        super().__init__(position, width, height)
        self.hasPowerup = False
        self.powerUp = None
        self.image = self.imgHandler.load(Box.image, (width, height))

    def update(self):
        pass


    def generatePowerUp(self):
        powerups = [RangePowerUp, BombNumPowerUp]
        self.powerUp = random.choice(powerups)
        self.hasPowerup = True

    def Destroy(self):
        i,j = self.position.y, self.position.x
        if self.hasPowerup:
            self.level.gameobjs[i][j] = self.powerUp(Point(self.position.x, self.position.y), self.level.bw, self.level.bh)
        else:
            self.level.gameobjs[i][j] = EmptySpace(self.position, self.level.bw, self.level.bh)