from .gameObject import GameObject
import os
from point import Point
from .wall import Wall
from .emptySpace import EmptySpace
from .powerup import *

class GameCharacter(GameObject):
    def __init__(self,position,speed):
        super().__init__(position, self.level.bw, self.level.bh)
        self.speed=speed


    def update(self):
        pass

    # def move(self,p, isPlayer=True):
    #     p= p.add(self.position)

    #     if(isinstance(self.level.gameobjs[p.y][p.x],EmptySpace)):

    #         if isPlayer:
    #             for pl in self.level.players:

    #                 if pl.position == p:
    #                     return False
    #                 # if (pl.position.x == p.x and pl.position.y == p.y):

    #                 #     return False

    #         self.position=p
    #         return True
    #     if (isinstance(self.level.gameobjs[p.y][p.x], PowerUp)):
    #         self.position = p
    #         if isPlayer:
    #             for pl in self.level.players:
    #                 if pl.position == p:
    #                     self.level.gameobjs[p.y][p.x].empower(pl)                    
    #                 # if(pl.position.x == p.x and pl.position.y == p.y):
    #                 #     print("Correct position")
    #                 #     self.level.gameobjs[p.y // self.level.bh][p.x // self.level.bw].empower(pl)


    #         return True

    #     return False