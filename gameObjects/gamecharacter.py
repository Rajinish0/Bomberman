from .gameobject import GameObject
import os

class GameCharacter(GameObject):
    def __init__(self,x,y,w,h,speed):
        super().__init__(x,y,w,h)
        self.speed=speed


    def update(self):
        pass

    def draw(self,display):
        pass