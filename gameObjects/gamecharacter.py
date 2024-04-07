from .gameObject import GameObject
import os
from point import Point
from .wall import Wall
from .emptySpace import EmptySpace

class GameCharacter(GameObject):
    def __init__(self,position,speed):
        super().__init__(position)
        self.speed=speed


    def update(self):
        pass

    def draw(self,display):
        pass

    def move(self,p, print_=False):
        p= p.mul(Point(self.level.bw, self.level.bh)).add(self.position)
        # if print_:
        #     print(p.x,p.y)
        #     print("hello")
        if(isinstance(self.level.gameobjs[p.y // self.level.bh][p.x // self.level.bw],EmptySpace)):
            # if print_:
            #     print("hello2")
            self.position=p
            return True

        return False